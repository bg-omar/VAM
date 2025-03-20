import pdfplumber
import re
import json
import pandas as pd


def extract_columns_using_positions(pdf_path):
    """
    Extracts structured data using fixed x0 positions for columns.
    Ensures each row has Quantity, Symbol, Value, Unit, and Uncertainty.
    Handles missing values by inheriting from previous rows.
    Detects subscripts and superscripts based on relative vertical positions.
    """
    extracted_data = []
    last_quantity = None  # Store last valid Quantity
    last_symbol = None  # Store last valid Symbol
    baseline_positions = {}  # Track baseline for symbols

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words_with_positions = page.extract_words()
            current_row = {"Quantity": "", "Symbol": "", "Value": "", "Unit": "", "Relative std. uncert.": ""}
            last_top = None  # Track last row position to group values

            # Define x0 ranges for each column based on observed positions
            column_positions = {
                "Quantity": (50, 230),  # Leftmost column
                "Symbol": (231, 280),
                "Value": (281, 420),
                "Unit": (421, 480),
                "Uncertainty": (481, 550)
            }

            for word in words_with_positions:
                x0 = word["x0"]
                text = word["text"].strip()
                top = word["top"]  # Track row grouping by vertical position
                bottom = word["bottom"]  # For detecting subscript/superscript

                # If the top value changes, it indicates a new row
                if last_top is not None and abs(top - last_top) > 5:
                    if current_row["Relative std. uncert."]:  # Only add valid rows
                        if not current_row["Quantity"]:
                            current_row["Quantity"] = last_quantity
                        if not current_row["Symbol"]:
                            current_row["Symbol"] = last_symbol

                        extracted_data.append(current_row.copy())

                        if current_row["Quantity"]:
                            last_quantity = current_row["Quantity"]
                        if current_row["Symbol"]:
                            last_symbol = current_row["Symbol"]

                    # Reset row data
                    current_row = {"Quantity": "", "Symbol": "", "Value": "", "Unit": "", "Relative std. uncert.": ""}
                    baseline_positions = {}

                # Detect subscripts and superscripts
                baseline = baseline_positions.get(x0, top)  # Default baseline is the first text in column
                if top > baseline + 2:  # Subscript if lower than baseline
                    text = f"_{{{text}}}"
                elif top < baseline - 2:  # Superscript if higher than baseline
                    text = f"^{{{text}}}"
                baseline_positions[x0] = baseline  # Update baseline reference

                # Assign word to correct column based on x0 position
                if column_positions["Quantity"][0] <= x0 <= column_positions["Quantity"][1]:
                    current_row["Quantity"] += " " + text if current_row["Quantity"] else text
                elif column_positions["Symbol"][0] <= x0 <= column_positions["Symbol"][1]:
                    current_row["Symbol"] += " " + text if current_row["Symbol"] else text
                elif column_positions["Value"][0] <= x0 <= column_positions["Value"][1]:
                    current_row["Value"] += " " + text if current_row["Value"] else text
                elif column_positions["Unit"][0] <= x0 <= column_positions["Unit"][1]:
                    current_row["Unit"] += " " + text if current_row["Unit"] else text
                elif column_positions["Uncertainty"][0] <= x0 <= column_positions["Uncertainty"][1]:
                    current_row["Relative std. uncert."] += " " + text if current_row["Relative std. uncert."] else text

                last_top = top  # Update last row position

    return extracted_data


def refine_latex_symbols(rows):
    """
    Ensures proper LaTeX formatting:
    - Adds spaces between symbols correctly.
    - Fixes common symbol combinations.
    """
    corrected_data = []
    for row in rows:
        latex_symbol = row["Symbol"]

        # Ensure proper LaTeX spacing
        latex_symbol = re.sub(r"(?<!\\)([a-zA-Z])(?=[A-Z\\])", r"\1 ", latex_symbol)

        # Fix common physics expressions using raw strings
        latex_symbol = latex_symbol.replace("\\hbarc", "\\hbar c ")
        latex_symbol = latex_symbol.replace("hcR", "h c R_\\infty ")
        latex_symbol = latex_symbol.replace("¯h", "\\hbar ")
        latex_symbol = latex_symbol.replace("h¯", "\\hbar ")

        row["LaTeX Symbol"] = latex_symbol
        corrected_data.append(row)

    return corrected_data


def fix_exponents(rows):
    """
    Ensures that expressions like `m c2` are correctly formatted as `m c^2`.
    """
    corrected_data = []
    for row in rows:
        quantity = re.sub(r"(\b[a-zA-Z]+)\s*(\d+)", r"\1^\2", row["Quantity"])
        quantity = re.sub(r"(\(?\w+\s*\d*\)?)\s*/\s*(\(?\w+\s*\d*\)?)", r"\\frac{\1}{\2}", quantity)

        symbol = re.sub(r"(\b[a-zA-Z]+)\s*(\d+)", r"\1^\2", row["Symbol"])
        latex_symbol = re.sub(r"(\b[a-zA-Z]+)\s*(\d+)", r"\1^\2", row["LaTeX Symbol"])
        latex_symbol = re.sub(r"(\(?\w+\s*\d*\)?)\s*/\s*(\(?\w+\s*\d*\)?)", r"\\frac{\1}{\2}", latex_symbol)
        corrected_data.append({
            "Quantity": quantity,
            "Symbol": symbol,
            "LaTeX Symbol": latex_symbol,
            "Value": row["Value"],
            "Unit": row["Unit"],
            "Relative std. uncert.": row["Relative std. uncert."]
        })
    return corrected_data


def save_json(data, filename="extracted_constants.json"):
    """Saves extracted data as a JSON file."""
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    pdf_path = "physics_constants_all.pdf"  # Update with actual PDF file path
    extracted_data = extract_columns_using_positions(pdf_path)
    refined_data = refine_latex_symbols(extracted_data)
    structured_constants_final_exponents = fix_exponents(refined_data)
    save_json(structured_constants_final_exponents)
