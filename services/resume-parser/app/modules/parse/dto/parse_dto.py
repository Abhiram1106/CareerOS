from pydantic import BaseModel


class ParseResponse(BaseModel):
    sections: list[dict]
    ats_flags: list[str]
    parse_warnings: list[str]
    char_count: int
