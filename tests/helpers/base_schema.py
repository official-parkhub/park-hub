from pydantic import BaseModel


class BaseSchema:
    def assert_params(
        self, *, data: dict, expected_schema: type[BaseModel], is_error: bool = False
    ):
        try:
            expected_schema.model_validate(data)
            if is_error:
                raise AssertionError(
                    "Expected schema validation to fail, but it passed."
                )
        except Exception as error:
            if not is_error:
                raise AssertionError(
                    f"Expected schema validation to pass, but it failed: {error}"
                )
            return

    def assert_multiple_params(
        self,
        *,
        data_list: list[tuple[str, dict, bool]],
        expected_schema: type[BaseModel],
    ):
        for name, data, is_error in data_list:
            try:
                self.assert_params(
                    data=data, expected_schema=expected_schema, is_error=is_error
                )
            except Exception as error:
                raise AssertionError(f"Error in {name}: {error}")

    def assert_schema_fields(self, schema: type[BaseModel], expected_fields: list[str]):
        actual_fields = list(schema.model_fields.keys())
        missing = set(expected_fields) - set(actual_fields)
        extra = set(actual_fields) - set(expected_fields)

        if missing or extra:
            raise AssertionError(
                f"Schema fields do not match.\n"
                f"Expected: {expected_fields}\n"
                f"Actual: {actual_fields}\n"
                f"Missing: {list(missing)}\n"
                f"Extra: {list(extra)}"
            )
