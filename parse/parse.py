import os
import re
from pathlib import Path
import json
import typing
from datetime import datetime
import multiprocessing
from parse.ocr_utils import OCRError, UnparseableDocument, PageCountParse


def write(out_dir="./", ex_dict={}):
    outname = Path(ex_dict["filename"]).stem + ".json"

    p = Path(out_dir)
    if not p.exists():
        p.mkdir()

    with open(p.joinpath(outname), "w") as fp:
        json.dump(ex_dict, fp)
    return True


from parse.pages import handle_pages
from parse.pdf_reader import get_fitz_doc_obj
from parse.file_utils import coerce_file_to_pdf
from parse.ocr import get_ocr_filename


def parse(
    f_name,
    ocr_missing_doc=False,
    num_ocr_threads=2,
    force_ocr=False,
    out_dir="./",
):
    print("running policy_analyics.parse on", f_name)
    try:
        doc_dict = {"filename": f_name.name}
        if ocr_missing_doc or force_ocr:
            f_name = get_ocr_filename(f_name, num_ocr_threads, force_ocr)
        if not str(f_name).endswith(".pdf"):
            f_name = coerce_file_to_pdf(f_name)
            doc_dict["filename"] = re.sub(r"\.[^.]+$", ".pdf", doc_dict["filename"])

        doc_obj = get_fitz_doc_obj(f_name)
        handle_pages(doc_obj, doc_dict)
        doc_obj.close()

        write(out_dir=out_dir, ex_dict=doc_dict)
    except Exception as e:
        print("ERROR in policy_analytics.parse:", e)


def pdf_to_json(
    source: str,
    destination: str,
    multiprocess: int = -1,
    ocr_missing_doc: bool = False,
    force_ocr: bool = False,
    num_ocr_threads: int = 2,
    batch_size: int = 100,
) -> None:
    """
    Converts input pdf file to json
    Args:
        source: A source directory to be processed.
        destination: A destination directory to be processed
        verify: Boolean to determine if output jsons are to be verified vs a json schema
        metadata: file path of metadata to be processed.
        multiprocess: Multiprocessing. Will take integer for number of cores,
        ocr_missing_doc: OCR non-OCR'ed files
        num_ocr_threads: Number of threads to use for OCR (per file)
    """

    if Path(source).is_file():
        print("Parsing Single Document")

        single_process(
            f_name,
            out_dir,
            ocr_missing_doc,
            num_ocr_threads,
            force_ocr,
        )

    else:
        process_dir(
            dir_path=source,
            out_dir=destination,
            multiprocess=multiprocess,
            ocr_missing_doc=ocr_missing_doc,
            force_ocr=force_ocr,
            num_ocr_threads=num_ocr_threads,
            batch_size=batch_size,
        )


def single_process(
    f_name,
    out_dir,
    ocr_missing_doc: bool = False,
    num_ocr_threads: int = 2,
    force_ocr: bool = False,
) -> None:
    """
    Args:
        data_inputs: named tuple of kind "parser_input", the necessary data inputs
    Returns:
    """

    # Logging is not safe in multiprocessing thread. Especially if its going to a file
    # Directly printing to screen is a temporary solution here
    m_id = multiprocessing.current_process()

    print(
        "%s - [INFO] - Processing: %s - Filename: %s"
        % (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f'")[:-4],
            str(m_id),
            Path(f_name).name,
        )
    )

    try:
        parse(
            f_name=f_name,
            ocr_missing_doc=ocr_missing_doc,
            num_ocr_threads=num_ocr_threads,
            force_ocr=force_ocr,
            out_dir=out_dir,
        )

    # TODO: catch this where failed files can be counted or increment shared counter (for mp)
    except (OCRError, UnparseableDocument, PageCountParse) as e:
        print(e)
        print(
            "%s - [ERROR] - Failed Processing: %s - Filename: %s"
            % (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f'")[:-4],
                str(m_id),
                Path(f_name).name,
            )
        )
        return

    print(
        "%s - [INFO] - Finished Processing: %s - Filename: %s"
        % (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f'")[:-4],
            str(m_id),
            Path(f_name).name,
        )
    )


def process_dir(
    dir_path: str,
    out_dir: str = "./",
    multiprocess: int = False,
    ocr_missing_doc: bool = False,
    force_ocr: bool = False,
    num_ocr_threads: int = 2,
    batch_size: int = 100,
):
    """
    Processes a directory of pdf files, returns corresponding Json files
    Args:
        parse_func: Parsing function called on the data
        dir_path: A source directory to be processed.
        out_dir: A destination directory to be processed
        multiprocess: Multiprocessing. Will take integer for number of cores
        ocr_missing_doc: OCR non-ocr'ed docs in place
        num_ocr_threads: Number of threads used for OCR (per doc)
    """

    p = Path(dir_path).glob("**/*")
    files = [
        x
        for x in p
        if x.is_file()
        and (
            x.suffix.lower() in (".pdf", ".html", ".txt")
            or (
                filetype.guess(str(x)) is not None
                and (
                    filetype.guess(str(x)).mime == "pdf"
                    or filetype.guess(str(x)).mime == "application/pdf"
                )
            )
        )
    ]
    data_inputs = [
        (f_name, out_dir, ocr_missing_doc, num_ocr_threads, force_ocr)
        for f_name in files
    ]

    print("Parsing Multiple Documents: %i", len(data_inputs))

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    if multiprocess != -1:
        # begin = time.time()
        if multiprocess == 0:
            pool = multiprocessing.Pool(processes=os.cpu_count(), maxtasksperchild=1)
        else:
            pool = multiprocessing.Pool(processes=int(multiprocess), maxtasksperchild=1)
        print("Processing pool: %s", str(pool))

        if ocr_missing_doc:
            # ReOCR PDF if need (ex: page is missing)
            start_ocr_time = datetime.now()
            start_ocr_time_display = start_ocr_time.strftime("%H:%M:%S")
            print("Start reOCR Time =", start_ocr_time_display)

            # How many elements each list should have # work around with issue on queue being over filled
            # using list comprehension
            process_list = [
                data_inputs[i * batch_size : (i + 1) * batch_size]
                for i in range((len(data_inputs) + batch_size - 1) // batch_size)
            ]

            total_num_files = len(data_inputs)
            reocr_count = 0
            for item_process in tqdm(process_list):
                with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
                    results = [
                        executor.submit(check_ocr_status_job_type, data[1])
                        for data in item_process
                    ]
                    for index, fut in enumerate(
                        concurrent.futures.as_completed(results)
                    ):
                        if not isinstance(fut, type(None)):
                            if fut.result() is not None:
                                ocrd_pdf = fut.result().get("successful_ocr")
                                if (
                                    is_pdf(str(item_process[index][1]))
                                    and not ocrd_pdf
                                    and not is_encrypted_pdf(
                                        str(item_process[index][1])
                                    )
                                ):
                                    reocr_count += 1
                                    kwargs = {  # "deskew": True if ocr_job_type == OCRJobType.FORCE_OCR else False,
                                        # "rotate_pages": True,
                                        # "use_threads":True,
                                        "bad_pages": fut.result().get("bad_page_nums")
                                    }
                                    try:
                                        print(
                                            f"[OCR] Attempt reOCR of pages {kwargs.get('bad_pages')}"
                                        )
                                        # TODO: This is not multi threaded -- we want to multithread and batch process!!!!!
                                        ocr = PDFOCR(
                                            input_file=item_process[index][1],
                                            output_file=item_process[index][1],
                                            ocr_job_type=fut.result().get(
                                                "ocr_job_type"
                                            ),
                                            ignore_init_errors=True,
                                            num_threads=num_ocr_threads,  # default=2
                                        )
                                        try:
                                            is_ocr = ocr.convert(**kwargs)
                                        except SubprocessOutputError as e:
                                            print(e)
                                            is_ocr = False
                                    except Exception as ex:
                                        print(ex)
                                        is_ocr = False

            end_ocr_time = datetime.now()
            end_ocr_time_dispaly = end_ocr_time.strftime("%H:%M:%S")
            total_ocr_time = end_ocr_time - start_ocr_time
            print("End  reOCR  Time =", end_ocr_time_dispaly)
            print("Total OCR Time:", total_ocr_time)
            print(
                f"Count of documents reOCRed / total: {reocr_count} / {total_num_files}"
            )
        # Process files
        pool.map(single_process, *data_inputs, batch_size)
    else:
        for item in data_inputs:
            single_process(*item)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    # TODO: actually track how many were successfully processed
    print("Documents parsed (or attempted): %i", len(data_inputs))
