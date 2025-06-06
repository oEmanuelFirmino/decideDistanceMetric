import sys

VALID_HTML_FILES = {
    "index.html",
    "chebyshevDistance.html",
    "correlationDistance.html",
    "cosineDistance.html",
    "diceDistance.html",
    "euclidianDistance.html",
    "hammingDistance.html",
    "hellingerDistance.html",
    "jaccardDistance.html",
    "mahalanobisDistance.html",
    "manhattanDistance.html",
    "minkowskiDistance.html",
}


def check_links_from_file(filepath_of_html, links_to_check_file):
    broken_links = []
    try:
        with open(links_to_check_file, "r") as f:
            links = [line.strip() for line in f if line.strip()]

        if not links:

            print(
                f"No links found to check in {filepath_of_html} via {links_to_check_file}."
            )
            return [], []

        for link in links:
            if link.startswith("https://") or link.startswith("http://"):
                continue
            if link not in VALID_HTML_FILES:
                broken_links.append(f"{filepath_of_html}: Broken link - {link}")
        return broken_links, []
    except FileNotFoundError:
        return [], [f"Could not find the temporary file: {links_to_check_file}"]
    except Exception as e:
        return [], [
            f"Error processing {links_to_check_file} for {filepath_of_html}: {str(e)}"
        ]


if __name__ == "__main__":
    html_filename_arg = sys.argv[1]
    temp_links_filename_arg = sys.argv[2]

    broken_links_found, errors_found = check_links_from_file(
        html_filename_arg, temp_links_filename_arg
    )

    if errors_found:
        for error in errors_found:
            print(f"ERROR: {error}")

    if broken_links_found:
        for broken_link in broken_links_found:
            print(broken_link)

    if not errors_found and not broken_links_found:

        if broken_links_found is not None and not broken_links_found:
            print(f"All links in {html_filename_arg} are correct.")
    elif not broken_links_found and errors_found:
        print(
            f"Could not verify all links in {html_filename_arg} due to errors, but no broken links found in successfully parsed links."
        )
