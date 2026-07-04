from filinglens.models.document_chunk import DocumentChunk


def test_document_chunk():

    chunk = DocumentChunk(
        id="1",
        company="TCS",
        year="FY2024",
        page=12,
        chunk=0,
        text="Hello",
    )

    assert chunk.company == "TCS"
    assert chunk.page == 12
