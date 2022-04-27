class SchemaValidator(object):
    def __init__(self,response={}):
        self.response = response

    def isTure(self):
        error_message = []
        allowed_output_format = {"json", "xml"}

        # Validation for address field
        try:
            address = self.response.get("address", None)
            if address is None:
                raise Exception("Error")
        except Exception as e:
            error_message.append("address field is required")

        # Validation for output_format field
        try:
            output_format = self.response.get("output_format", None)
            if output_format is None:
                raise Exception("Error")
            else:
                try:
                    # check for valid output format
                    if output_format not in allowed_output_format:
                        raise Exception("Error")
                except Exception as e:
                    error_message.append(f"Inavlid output format:'{output_format}'. Only allowed format are {allowed_output_format}")
        except Exception as e:
            error_message.append("output_format field is required")

        return error_message