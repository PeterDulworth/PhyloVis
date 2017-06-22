from collections import defaultdict

def is_informative(site):
    """
    Determines if a site is informative or not
    Input:
    site --- a list of bases located at a site in the alignment 
    Output:
    1 if a site is informative 0 if a site is uninformative
    """

    # Create a mapping of bases to the number of times they occur
    base_to_counts = defaultdict(int)

    # Iterate over each base in the list site
    for base in site:

        # Add one each time a base occurs
        base_to_counts[base] += 1

    # Create a list of counts in descending order
    base_counts = sorted(base_to_counts.values(), reverse=True)
    print base_counts

    # If two different bases occur at least twice the site is informative
    if (base_counts[0] >= 2) and (base_counts[1] >= 2):
        return 1

    else:
        return 0

