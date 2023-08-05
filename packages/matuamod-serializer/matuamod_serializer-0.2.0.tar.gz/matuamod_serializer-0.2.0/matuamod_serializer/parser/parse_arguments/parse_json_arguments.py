right_brace = "right_brace"
left_brace = "left_brace"
right_bracket = "right_bracket"
left_bracket = "left_bracket"
comma = "comma"
colon = "colon"
none = "null"
number = "number"
str_arg = "str"
bool_arg = "bool"
eof = "eof"


parse_arg = {
    right_brace: r"{",
    left_brace: r"}",
    right_bracket: "\\[",
    left_bracket: "\\]",
    comma: r",",
    colon: r":",
    none: r"null",
    number: r'([0-9]*[.])?[0-9]+',
    str_arg: r'"[^"]*"',
    bool_arg: r'^(?:tru|fals)e',
    eof: r"eof"
}
    

