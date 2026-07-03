from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json


class Chunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def process_folder(
        self,
        text_folder,
        output_folder,
        company,
        year,
    ):

        text_folder = Path(text_folder)
        output_folder = Path(output_folder)

        output_folder.mkdir(parents=True, exist_ok=True)

        for txt_file in sorted(text_folder.glob("*.txt")):

            page = int(txt_file.stem.split("_")[1])

            text = txt_file.read_text(
                encoding="utf-8"
            )

            chunks = self.splitter.split_text(text)

            for i, chunk in enumerate(chunks):

                output = {

                    "company": company,

                    "year": year,

                    "page": page,

                    "chunk": i,

                    "text": chunk

                }

                with open(
                    output_folder /
                    f"{txt_file.stem}_{i}.json",
                    "w",
                    encoding="utf-8",
                ) as f:

                    json.dump(
                        output,
                        f,
                        indent=4,
                        ensure_ascii=False,
                    )

        print("Chunking complete.")