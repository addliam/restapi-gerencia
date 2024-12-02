import io
import csv


class Csvformatter:
    def __init__(self) -> None:
        pass

    def format(self, result):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=result[0].keys())

        writer.writeheader()
        writer.writerows(result)

        contenido_csv = output.getvalue()
        output.close()
        return contenido_csv
