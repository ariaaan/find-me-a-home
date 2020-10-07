"""New listings."""
import os
import glob
import json
import argparse
import jsonlines


def parse_arguments():
    parser = argparse.ArgumentParser(description='new-listings')
    parser.add_argument('listing_folder', help='path for the listing folder')
    parser.add_argument('output_folder', help='path for the output folder')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()

    listing_files = sorted(
        glob.glob(
            os.path.join(
                args.listing_folder,
                '*.jsonl'
            )
        )
    )

    for listing_1, listing_2 in zip(
        listing_files,
        listing_files[1:],
    ):
        date_1 = os.path.basename(listing_1).split('_')[0]
        date_2 = os.path.basename(listing_2).split('_')[0]

        with jsonlines.open(listing_1) as reader:
            listings_urls_date_1 = [
                item['url'] for item in list(reader)
            ]

        with jsonlines.open(listing_2) as reader:
            listings_urls_date_2 = [
                item['url'] for item in list(reader)
            ]

        new_listings = [
            url for url in listings_urls_date_2
            if url not in listings_urls_date_1
        ]

        new_listings_output_path = os.path.join(
            args.output_folder,
            f'{date_2}_new-listings.json'
        )

        json.dump(
            new_listings,
            open(new_listings_output_path, 'w'),
        )
