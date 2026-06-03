import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

EMAILS = [
    """
    From: Sarah Whitfield <s.whitfield@gmail.com>
    Subject: 24 Maple Court — viewing

    Hi, I saw the 2-bed flat at 24 Maple Court advertised at £1,450 pcm.
    I'd love to arrange a viewing this week if possible —
    I'm free Thursday or Friday afternoon.
    My number is 07700 900112.

    Thanks,
    Sarah
    """,

    """
    From: mike <mikejtt@outlook.com>
    Subject: flat

    is the place still available?
    interested in renting asap.
    can you call me

    Thanks
    """,

    """
    From: Daniel O. <d.osei@workmail.com>
    Subject: Re: Fwd: properties

    hi there hope ur well — quick one,
    im after either the studio on hartley road
    or the one bed on the high street whichever comes up first,
    budget around 1100,
    you can reach me on 07911 123456 or this email,
    also do you take housing benefit?

    cheers dan

    Sent from my iPhone

    On Mon, 12 May, Lettings Team wrote:
    > Please find attached our latest availability list
    >>> [image removed]
    >>> 020 7946 0000
    """,

    """
    From: Priya N <priya.nair88@gmail.com>
    Subject: Enquiry

    Hello.
    I am interested for the apartment.
    Please send more details and when I can see it.

    Thank you.
    """,

    """
    From: James Carter <jcarter.property@gmail.com>
    Subject: Three Oaks Road + parking

    Morning — two things.

    First, is 12 Three Oaks Road (the 3-bed)
    still on at £2,100?

    And does it come with a parking space,
    or is that extra?

    If it's available I'd want to move for 1st July.

    Mobile 07700 900345,
    or reply here.

    James Carter,
    07700 900345
    """
]


SYSTEM_PROMPT = """
You are an information extraction engine.

Extract the following fields:

- enquirer_name
- property
- enquiry_type
- email
- phone
- enquiry_summary

Rules:

enquiry_type must be one of:
- viewing
- availability
- general_question

Return JSON only.

If a field cannot be determined,
return null.

Do not invent information.
"""


def extract_email(email_text):

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": email_text
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )


def validate(record):

    flags = []

    if not record.get("enquirer_name"):
        flags.append("missing_name")

    if not record.get("property"):
        flags.append("missing_property")

    if (
        not record.get("email")
        and not record.get("phone")
    ):
        flags.append("missing_contact")

    record["flags"] = flags
    record["requires_manual_review"] = len(flags) > 0

    return record


def process_emails():

    results = []

    for i, email in enumerate(EMAILS, start=1):

        extracted = extract_email(email)

        validated = validate(extracted)

        validated["email_id"] = i

        results.append(validated)

    return results


if __name__ == "__main__":

    output = process_emails()

    print(
        json.dumps(
            output,
            indent=2
        )
    )

    with open("output.json", "w") as f:
        json.dump(
            output,
            f,
            indent=2
        )

    print("\nSaved to output.json")