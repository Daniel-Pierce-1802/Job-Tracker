import csv
import sys
from rich.console import Console
from rich.table import Table
from rich import box
import os

def init_file():
    if not os.path.exists("job_tracker.csv"):
        with open("job_tracker.csv", "w", newline="") as f:
            fieldnames = ["Company", "Job Title", "Date", "Status"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def add_job():
    company_name = input("Company Name: ")
    job_title = input("Job Title: ")
    date = input("Date: ")
    status = input("Status: ")
    with open("job_tracker.csv", "a") as f:
        fieldnames = ["Company", "Job Title", "Date", "Status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(
            {
                "Company": company_name,
                "Job Title": job_title,
                "Date": date,
                "Status": status,
            }
        )


def view_jobs():
    with open("job_tracker.csv", "r") as f:
        contents = csv.DictReader(f, delimiter=",")
        applications = list(contents)

        STATUS_COLORS = {
            "Applied": "cyan",
            "Interviewed": "yellow",
            "Offer": "green",
            "Rejected": "red",
        }

    console = Console()
    table = Table(box=box.ROUNDED, show_lines=True)

    table.add_column("Company")
    table.add_column("Job Title")
    table.add_column("Date")
    table.add_column("Status")

    for row in applications:
        color = STATUS_COLORS.get(row["Status"], "white")
        table.add_row(
            row["Company"],
            row["Job Title"],
            row["Date"],
            f"[{color}]{row['Status']}[/{color}]",
        )

    console.print(table)


def search():
    job = input("Company Name: ")
    with open("job_tracker.csv", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        applications = list(reader)

        STATUS_COLORS = {
            "Applied": "cyan",
            "Interviewed": "yellow",
            "Offer": "green",
            "Rejected": "red",
        }

    console = Console()
    table = Table(box=box.ROUNDED, show_lines=True)

    table.add_column("Company")
    table.add_column("Job Title")
    table.add_column("Date")
    table.add_column("Status")

    found = False
    for row in applications:
        color = STATUS_COLORS.get(row["Status"], "white")
        if job == row["Company"]:
            found = True
            table.add_row(
                row["Company"],
                row["Job Title"],
                row["Date"],
                f"[{color}]{row['Status']}[/{color}]",
            )
    console.print(table)
    if not found:
        print("Company name not found")


def edit_status():
    job = input("Company Name: ")
    new_status = input("New Status: ")
    with open("job_tracker.csv", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        applications = list(reader)
        for row in applications:
            if job == row["Company"]:
                row.update({"Status": new_status})

    with open("job_tracker.csv", "w") as f:
        fieldnames = ["Company", "Job Title", "Date", "Status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(applications)


def one_commandline_limit():
    if len(sys.argv) < 2:
        sys.exit("Too few command line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command line arguments")

    commands = ["add", "view", "search", "edit"]
    if sys.argv[1] not in commands:
        sys.exit("Command not recognized. Valid commands: add, view, search, edit")


def main():
    init_file()
    one_commandline_limit()
    if sys.argv[1] == "add":
        add_job()
    elif sys.argv[1] == "view":
        view_jobs()
    elif sys.argv[1] == "search":
        search()
    elif sys.argv[1] == "edit":
        edit_status()


if __name__ == "__main__":
    main()
