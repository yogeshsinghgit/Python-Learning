
data = """Timeline With almost 50 years in the tech industry and 40 in the UK, we've continuously focussed on helping everyone achieve more. Explore a timeline of our journey. 1975 - 1999 2000 - 2009 2010 - 2019 2020 - Present APR 4, 1975 Microsoft founded AUG 12, 1981 IBM introduces its personal computer with Microsoft's 16-bit operating system MS-DOS 1.0 Microsoft UK launches First version of Windows announced First version of Office announced AUG 24, 1995 Launches Windows 95 DEC 7, 1995 Bill Gates outlines Microsoft's commitment to supporting and enhancing the internet JAN 13, 2000 Steve Ballmer named president and CEO for Microsoft OCT 25, 2001 Launches Windows XP NOV 15, 2001 Xbox launched - Discover the history of Xbox JAN 15, 2002 Bill Gates outlines Microsoft's commitment to trustworthy computing MAY 28, 2009 Microsoft unveils Bing OCT 22, 2009 Launches Windows 7 JUN 28, 2011 Office 365 launches JUN 18, 2012 Surface devices launched JUN 30, 2012 Michel Van der Bel becomes Microsoft UK CEO OCT 26, 2012 Windows 8 launched FEB 4, 2014 Satya Nadella becomes Microsoft CEO - Read Satya's bio and latest news JAN 21, 2015 HoloLens , the world's first holographic headset is announced JUL 29, 2015 Windows 10 launched JUN 30, 2016 Cindy Rose becomes Microsoft UK CEO SEP 29, 2016 Microsoft Research AI launched JUL, 2017 AI for Good announced to help empower those working to solve humanitarian issues - Discover how MAY 16, 2018 Microsoft unveils Xbox Adaptive Controller JUN 1, 2018 Underwater data centre deployed JUL 11, 2019 London flagship store opens JAN 16, 2020 Microsoft announces goal to be net zero by 2030 APR 15, 2020 Microsoft announces plan to help protect biodiversity of the world's ecosystems APR 4, 2020 Microsoft's 45th anniversary JUL 2020 Microsoft helps British manufacturers unite to build ventilators for the NHS in just 12 weeks NOV 10, 2020 Launches Xbox Series X OCT 1, 2020 Clare Barclay announced as Microsoft UK CEO OCT 13, 2020 Microsoft launches 5-year campaign to help 1.5 million people build tech careers in the UK - Read about Get On JUL 14, 2021 Microsoft unveils Windows 365 OCT 5, 2021 Windows 11 launches OCT 11, 2021 First digital billboards to feature BSL in the UK to showcase our commitment to accessibility NOV 2021 Microsoft is the primary partner at COP26 NOV 18, 2021 The Duke of Cambridge visits Microsoft's UK headquarters to hear about Project SEEKR JAN 17, 2022 Hector Minto, Lead Evangelist for Accessibility at Microsoft UK announced as Government Disability and Access Ambassador for Tech and Web JAN 2022 Microsoft unveils accelerator for startups that use technology to help the planet FEB 2022 Chancellor Rishi Sunak visits Microsoft's UK HQ and highlights impact of apprentices on economy MAR 2022 Microsoft appoints Musidora Jorgensen to UK leadership team JUN 2022 Launch of Microsoft Cloud for Sustainability SEP 2022 Campaign to raise awareness of how technology can help with Dyslexia DEC 2022 Announced 10-year strategic partnership with the London Stock Exchange Group (LSEG) JUN 2023 A new five-year deal delivers Microsoft 365 productivity tools to NHS England OCT 2023 Microsoft expands its UK skilling programme to equip 1 million people for the AI-based economy
"""

from datetime import datetime
import re

def filter_content_as_per_dates(content, n_years):
    """
    Filters the content to include only events within the last `n_years` from the current year.
    
    Args:
        content (str): The text data containing event timeline.
        n_years (int): Number of years to look back from the current year.
    
    Returns:
        str: Filtered content with only relevant date range.
    """
    current_year = datetime.now().year
    min_year = current_year - n_years

    # Extract sentences that contain a year within the desired range
    filtered_lines = []
    for line in content.split("."):
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', line)  # Find years in the line
        if any(min_year <= int(year) <= current_year for year in years):
            filtered_lines.append(line)

    return "\n".join(filtered_lines)

# Test the function
print(len(data.split()))
result = filter_content_as_per_dates(content=data, n_years=10)
print(result, len(result.split()))