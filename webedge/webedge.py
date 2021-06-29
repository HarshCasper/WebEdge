import json
import argparse
from webedge import website_analysis
from webedge import cli_output
import sys

def create_parser():
    """
        Creates a Parser to pass Arguement Parser.
        Returns:
            parser: Arguement Parser through which the User can pass the Website
        """
    parser = argparse.ArgumentParser(
        description='Search and Analyze the Search Engine Optimization of a Website'
    )
    parser.add_argument(
        '-d', '--domain', type=str, required=True,
        help='Share the Website Domain to analyze'
    )
    parser.add_argument(
        '-s', '--sitemap', type=str, required=False,
        help='Sitemap.xml file to use'
    )

    parser.add_argument(
        '-p', '--page', type=str, required=False,
        help='Single Page to analyze'
    )
    return parser
def analyze(domain, sitemap, page):
    """
        Analyzes the Domain/Sitemap/Page passed by the User.
        Args:
            domain: Uniform Resource Locator of the Web Application
            sitempap: An XML Sitemap for a Web Application
            page: Uniform Resource Locator for a single Webpage
        Returns:
            report: JSON Document consisting of all achievements and warnings
        """
    spider = website_analysis.Spider(domain, sitemap, page)
    raw_report = spider.crawl()
    return json.dumps(raw_report, indent=4, separators=(',', ': '))

def main():
    """
        Main Function to run the Parser and invoke the Scripts.
        Returns:
            report: JSON Report of the whole Website/Webpage/Sitemap
    """
    cli_output.outputName("WebEdge")
    parser = create_parser()
    args = parser.parse_args()
    err = False
    cli_output.startLoading()
    try:
        report = analyze(args.domain, args.sitemap, args.page)
    except (SystemExit,KeyError) :
        cli_output.exitError()
        err = True
    except: #skipcq FLK-E722
        cli_output.printError(str(sys.exc_info()[0])+"\n"+str(sys.exc_info()[1]))
        cli_output.outputError()
        err = True
    try:
        cli_output.endLoading()
    except: #skipcq FLK-E722
        sys.exit()
    try:
        if not err:
            cli_output.outputJson(report)
    except (SystemExit,KeyError) :
        cli_output.exitError()
    except: #skipcq FLK-E722
        cli_output.printError(str(sys.exc_info()[0])+"\n"+str(sys.exc_info()[1]))
        cli_output.outputError()

if __name__ == "__main__":
    main()
