from typing import List, Tuple


class ConditionParser:
    def __init__(self, conditions: dict, field_quote: str = ""):
        self.conditions = conditions
        self.field_quote = field_quote

    def condition_interpretation(self, conditions: dict) -> Tuple[List, str]:
        parsed_conditions = []
        logical_operator = None

        for c in conditions.keys():
            if c[0] == "$":
                if c == "$type":
                    logical_operator = conditions[c]

                if c == "$group":
                    cond = self.condition_interpretation(conditions[c])
                else:
                    cond = []

            else:
                cond = self.condition(c, conditions[c])

            parsed_conditions.extend(cond)

        return parsed_conditions, logical_operator

    def condtion_parser(self, conditions: dict, logical_operator: str = "AND") -> str:
        parsed_conditions = []
        logical_operator = logical_operator if len(conditions) > 0 else ""

        for c in conditions.keys():
            if c == "$group":
                group = self.condition_interpretation(
                    conditions[c]
                )
                group_parsed = f' {group[1]} '.join(group[0])
                group_parsed = f"({group_parsed})"
                parsed_conditions.append(
                    group_parsed
                )
            else:
                parsed_conditions.extend(
                    self.condition(c, conditions[c])
                )

        if len(parsed_conditions) == 0:
            return ""

        return f"{f' {logical_operator} '.join(parsed_conditions)}"

    def condition(self, field_name: str, field_condition: dict) -> List:
        conditions = []
        for fc in field_condition.keys():
            if fc == "$value":
                parse = f"{self.field_quote}{field_name}{self.field_quote} = '{field_condition[fc]}'"
                conditions.append(parse)
            if fc == "$like":
                parse = f"{self.field_quote}{field_name}{self.field_quote} LIKE '{field_condition[fc]}'"
                conditions.append(parse)
            if fc == "$in":
                in_fields = "','".join(field_condition[fc].split(','))
                parse = f"{self.field_quote}{field_name}{self.field_quote} IN ('{in_fields}')"
                conditions.append(parse)
            if fc == "$nin":  # TODO: Add support for type to be list instead of str and split by , and support for SQL
                in_fields = "','".join(field_condition[fc].split(','))
                parse = f"{self.field_quote}{field_name}{self.field_quote} NOT IN ('{in_fields}')"
                conditions.append(parse)

        return conditions

    def get_parsed(self):
        parse = self.condtion_parser(
            self.conditions
        )
        return parse