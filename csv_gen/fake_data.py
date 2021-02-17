import names
import random
import string
from faker import Faker


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


fake = Faker()

JOBS = [
    "Director",
    "Manager",
    "Administrator",
    "Architect",
    "Representative",
    "Specialist",
    "Boss",
    "President",
    "Vice-president",
    "Partner",
    "Leader",
    "Coordinator",
    "Engineer",
    "Officer",
    "Analyst",
    "Consultant",
    "Advisory",
    "Estimator",
    "Professional",
    "Supervisor",
    "Messenger",
    "Executive",
    "Agent",
    "Appraiser",
    "Economist",
    "Controller",
    "Counsel",
    "Underwriter",
    "Broker",
    "Operator",
    "Superintendent",
    "Surveyor",
    "Researcher"
]


def random_full_name(*args):
    return names.get_full_name()


def random_job(*args):
    return random.choice(JOBS)


def random_email(*args):
    return random_char(7) + "@gmail.com"


def random_domain_name(*args):
    return random_char(8) + ".com"


def random_phone_number(*args):
    number = '+380'
    number += ''.join([str(random.randint(1, 9)) for i in range(9)])
    return number


def random_company_name(*args):
    return random_char(10)


def random_text(col_filter):
    sent_number = col_filter.get('length', 4)
    return fake.paragraph(nb_sentences=sent_number)


def random_integer(col_filter):
    nmb_to = col_filter.get('to', 100)
    nmb_from = col_filter.get('from', 0)
    return random.randint(nmb_from, nmb_to)


def random_address(col_filter):
    return fake.address().replace('\n', ' ')


def random_date(col_filter):
    return str(fake.date_between(start_date='today', end_date='+30y'))


FAKE_DATA_GENERATOR = {
    'Full name': random_full_name,
    'Job': random_job,
    'Email': random_email,
    'Domain name': random_domain_name,
    'Phone number': random_phone_number,
    'Company name': random_company_name,
    'Text': random_text,
    'Integer': random_integer,
    'Address': random_address,
    'Date': random_date,
}
