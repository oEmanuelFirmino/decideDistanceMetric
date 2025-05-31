import re
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
}

def find_all_links_in_block(html_block_content):
    if not html_block_content:
        return []
    try:
        links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html_block_content)
        return links
    except Exception as e:
        # This should ideally not happen with findall unless pattern is malformed
        print(f"Regex error in find_all_links_in_block: {e}")
        return []

def check_links(filepath, full_html_content):
    broken_links = []
    errors = []

    # Clean the HTML content from the markers if they exist
    full_html_content = re.sub(r'^\[start of [^\]]+\]\n?', '', full_html_content)
    full_html_content = re.sub(r'\n?\[end of [^\]]+\]$', '', full_html_content)

    # 1. Check navigation menu links
    # The navigation menu is the first major div after <body> or within a <nav> that was replaced.
    # It starts with <div class="bg-teal-600 text-white shadow-md"> and ends before <main>
    # For robustness, we find this block first.
    nav_menu_search_pattern = r'(<div class="bg-teal-600 text-white shadow-md">.*?(?:</div>\s*</div>\s*</div>\s*</div>))' # Matches the whole nav structure
    nav_menu_match = re.search(nav_menu_search_pattern, full_html_content, re.DOTALL)

    if nav_menu_match:
        nav_html_block = nav_menu_match.group(1)
        nav_links = find_all_links_in_block(nav_html_block)
        if not nav_links:
            errors.append(f"{filepath}: No links found in identified Navigation Menu block.")
        for link in nav_links:
            if link not in VALID_HTML_FILES:
                broken_links.append(f"{filepath} (Navigation Menu): Broken link - {link}")
    else:
        errors.append(f"{filepath}: Navigation Menu section not found with pattern: {nav_menu_search_pattern}")

    # 2. Specifically for index.html, check "Explore as Métricas" section
    if filepath == "index.html":
        metric_section_search_pattern = r'(<section id="metric-links".*?</section>)'
        metric_section_match = re.search(metric_section_search_pattern, full_html_content, re.DOTALL)

        if metric_section_match:
            metric_html_block = metric_section_match.group(1)
            metric_links = find_all_links_in_block(metric_html_block)
            if not metric_links:
                errors.append(f"{filepath}: No links found in identified 'Explore as Métricas' section.")
            for link in metric_links:
                if link not in VALID_HTML_FILES:
                    broken_links.append(f"{filepath} (Explore as Métricas): Broken link - {link}")
        else:
            errors.append(f"{filepath}: 'Explore as Métricas' section not found.")

    return broken_links, errors

# Main execution
if __name__ == "__main__":
    file_content_to_check = sys.stdin.read()
    file_path_to_check = sys.argv[1]

    broken_links_found, errors_found = check_links(file_path_to_check, file_content_to_check)

    if errors_found:
        for error in errors_found:
            print(f"ERROR: {error}")

    if broken_links_found:
        for broken_link in broken_links_found:
            print(broken_link)

    if not errors_found and not broken_links_found:
        print(f"All links in {file_path_to_check} are correct.")
    elif not broken_links_found and errors_found:
        # If only errors in finding sections, but no broken links found in sections that WERE found
        print(f"Could not verify all sections in {file_path_to_check} due to errors, but no broken links found in successfully parsed sections.")
