import argparse
import logging
import multiprocessing
import os
from typing import Union
from nbtlib import CompoundSchema, File, load, schema
from nbtlib.tag import Compound, Int, List, String
from tqdm import tqdm

SCHEMATIC_VERSION = 2586

def structure_schema() -> CompoundSchema:
    return schema(
        "Structure",
        {
            "DataVersion": Int,
            "author": String,
            "size": List[Int],
            "palette": List[
                schema(
                    "State",
                    {
                        "Name": String,
                        "Properties": Compound,
                    },
                )
            ],
            "blocks": List[
                schema(
                    "Block",
                    {
                        "state": Int,
                        "pos": List[Int],
                        "nbt": Compound,
                    },
                )
            ],
        },
    )()

def get_schematic_size(worldedit: File) -> dict:
    s = worldedit["Schematic"]
    return {
        "x": int(s["Length"]),
        "y": int(s["Height"]),
        "z": int(s["Width"]),
    }

def initiate_schema(worldedit: File) -> CompoundSchema:
    nbt_schematic = structure_schema()
    nbt_schematic["DataVersion"] = SCHEMATIC_VERSION
    nbt_schematic["palette"] = []
    nbt_schematic["blocks"] = []
    nbt_schematic["author"] = "Folfy_Blue"
    size = get_schematic_size(worldedit)
    nbt_schematic["size"] = [size["x"], size["y"], size["z"]]
    return nbt_schematic

def get_block_palette(worldedit: File) -> dict:
    # Mapeamento simples: ID -> minecraft:unknown_ID
    palette = {}
    for i in range(256):
        palette[i] = f"minecraft:unknown_{i}"
    return palette

def process_block_palette(nbt_schematic: CompoundSchema, byte_palette: dict) -> tuple:
    new_palette = {}
    for block_id, block in byte_palette.items():
        block_name = block
        bp = {}
        nbt_schematic["palette"].append({"Name": block_name, "Properties": bp})
        new_palette[block] = len(nbt_schematic["palette"]) - 1
    return nbt_schematic, new_palette

def process_block_entities(worldedit: File) -> dict:
    block_entities = {}
    s = worldedit["Schematic"]
    if "TileEntities" in s:
        for data in s["TileEntities"]:
            d = data.copy()
            x, y, z = d['x'], d['y'], d['z']
            key = f"{x} {y} {z}"
            block_entities[key] = d
    return block_entities

def process_blocks(
    worldedit: File,
    nbt_schematic: CompoundSchema,
    byte_palette: dict,
    new_palette: dict,
    block_entities: dict = {},
    queue: Union[multiprocessing.Queue, None] = None,
) -> CompoundSchema:
    s = worldedit["Schematic"]
    size = get_schematic_size(worldedit)
    blocks = s["Blocks"]
    width = size["z"]
    length = size["x"]
    height = size["y"]
    for y in range(height):
        for z in range(width):
            for x in range(length):
                i = y * width * length + z * length + x
                block_id = blocks[i]
                # Corrige IDs negativos para o intervalo 0-255
                if isinstance(block_id, int) and block_id < 0:
                    block_id += 256
                block_name = byte_palette.get(block_id, f"minecraft:unknown_{block_id}")
                key = f"{x} {y} {z}"
                block_nbt = block_entities.get(key, None)
                block_entry = {
                    "state": new_palette[block_name],
                    "pos": [x, y, z]
                }
                if block_nbt:
                    block_entry["nbt"] = block_nbt
                nbt_schematic["blocks"].append(block_entry)
                if queue:
                    queue.put(True)
    return nbt_schematic

def process_file(
    input_file: str, output_file: str, queue=Union[multiprocessing.Queue, None]
) -> None:
    logging.info(f"Processing {input_file}...")
    try:
        with load(input_file) as worldedit:
            nbt_schematic = initiate_schema(worldedit)
            block_entities = process_block_entities(worldedit)
            byte_palette = get_block_palette(worldedit)
            nbt_schematic, new_palette = process_block_palette(
                nbt_schematic, byte_palette
            )
            nbt_schematic = process_blocks(
                worldedit=worldedit,
                nbt_schematic=nbt_schematic,
                byte_palette=byte_palette,
                new_palette=new_palette,
                block_entities=block_entities,
                queue=queue,
            )
        logging.info(f"Saving {output_file}...")
        File({"": Compound(nbt_schematic)}, gzipped=True).save(output_file)
    except Exception as e:
        logging.error(f"An error occurred while processing {input_file}: {repr(e)}")

def process_files(input_files: list, output_files: list) -> None:
    queue = multiprocessing.Queue()
    processes = []
    total_blocks = 0
    for input_file in input_files:
        with load(input_file) as worldedit:
            total_blocks += len(worldedit["Schematic"]["Blocks"])
    with tqdm(total=total_blocks, desc="Blocks processed") as pbar:
        for input_file, output_file in zip(input_files, output_files):
            process = multiprocessing.Process(
                target=process_file, args=(input_file, output_file, queue)
            )
            processes.append(process)
            process.start()
        while any(process.is_alive() for process in processes):
            while not queue.empty():
                queue.get()
                pbar.update()
        for process in processes:
            process.join()
        pbar.close()

def process_paths(args: argparse.Namespace) -> tuple:
    input_files, output_files = [], []
    if args.folder:
        if not os.path.exists(args.input):
            logging.error(f"Folder '{args.input}' not found.")
            exit(1)
        if not args.output:
            args.output = args.input
        os.makedirs(args.output, exist_ok=True)
        file_list = [
            f
            for f in os.listdir(args.input)
            if os.path.isfile(os.path.join(args.input, f))
        ]
        input_files = [os.path.join(args.input, f) for f in file_list]
        output_files = [
            os.path.join(args.output, f"{os.path.splitext(f)[0]}.nbt")
            for f in file_list
        ]
    else:
        if not os.path.isfile(args.input):
            logging.error(f"File '{args.input}' not found.")
            exit(1)
        input_files = [args.input]
        output_files = [args.output or f"{os.path.splitext(args.input)[0]}.nbt"]
    return input_files, output_files

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte arquivos .schematic do WorldEdit para .nbt do Structure Block (Create mod)."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Caminho do arquivo .schematic de entrada ou pasta.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        default=None,
        help="Caminho do arquivo .nbt de saída ou pasta.",
    )
    parser.add_argument(
        "-f",
        "--folder",
        action="store_true",
        default=False,
        help="Converter todos os arquivos de uma pasta.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Exibir logs detalhados.",
    )
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.CRITICAL)
    input_files, output_files = process_paths(args)
    process_files(input_files, output_files)

if __name__ == "__main__":
    main()
