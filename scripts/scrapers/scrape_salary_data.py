"""
AI Salary Data Web Scraper for Canada
======================================
This script demonstrates web scraping techniques for collecting AI salary data
from various job boards and salary websites.

Requirements:
pip install requests beautifulsoup4 pandas selenium webdriver-manager lxml

Note: Always check robots.txt and Terms of Service before scraping.
Use responsibly with appropriate delays between requests.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime
import re
from typing import List, Dict
import random
from pathlib import Path

class AISalaryScraper:
    def __init__(self, output_dir='data/real_data'):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.results = []
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def delay(self, min_seconds=2, max_seconds=5):
        """Add random delay to be respectful to servers"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def scrape_indeed_ca(self, job_title="AI Engineer", location="Canada", max_pages=3):
        """
        Scrape Indeed.ca for job listings
        Note: Indeed's structure changes frequently
        """
        print(f"\n🔍 Scraping Indeed.ca for {job_title} in {location}...")
        base_url = "https://ca.indeed.com/jobs"
        
        for page in range(max_pages):
            try:
                params = {
                    'q': job_title,
                    'l': location,
                    'start': page * 10
                }
                
                response = self.session.get(base_url, params=params, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards (structure may vary)
                job_cards = soup.find_all('div', class_=re.compile('job_seen_beacon|jobsearch-SerpJobCard'))
                
                for card in job_cards:
                    try:
                        # Extract title
                        title_elem = card.find('h2', class_=re.compile('jobTitle'))
                        title = title_elem.get_text(strip=True) if title_elem else 'N/A'
                        
                        # Extract company
                        company_elem = card.find('span', class_=re.compile('companyName'))
                        company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                        
                        # Extract location
                        location_elem = card.find('div', class_=re.compile('companyLocation'))
                        job_location = location_elem.get_text(strip=True) if location_elem else 'N/A'
                        
                        # Extract salary if available
                        salary_elem = card.find('div', class_=re.compile('salary-snippet'))
                        salary = salary_elem.get_text(strip=True) if salary_elem else 'Not Listed'
                        
                        self.results.append({
                            'source': 'Indeed.ca',
                            'job_title': title,
                            'company': company,
                            'location': job_location,
                            'salary': salary,
                            'search_term': job_title,
                            'scraped_date': datetime.now().strftime('%Y-%m-%d')
                        })
                    except Exception as e:
                        print(f"  ⚠️  Error parsing job card: {e}")
                        continue
                
                print(f"  ✓ Scraped page {page + 1}")
                self.delay()
                
            except Exception as e:
                print(f"  ✗ Error scraping page {page + 1}: {e}")
                continue
    
    def scrape_glassdoor_api_alternative(self):
        """
        Note: Glassdoor heavily protects against scraping.
        This demonstrates the concept but may not work without authentication.
        Consider using their official API if available.
        """
        print("\n🔍 Attempting Glassdoor data collection...")
        print("  ℹ️  Glassdoor requires authentication and has strict anti-scraping measures.")
        print("  ℹ️  Consider using their official API or manual data collection instead.")
        
        # Placeholder for demonstration
        # In practice, you'd need to handle authentication, JavaScript rendering, etc.
        return
    
    def scrape_job_bank_ca(self, job_code="21211"):
        """
        Scrape Government of Canada Job Bank
        Note: Job Bank has public data and is more scraping-friendly
        NOC 21211 = Data Scientists
        NOC 21231 = Software Engineers
        """
        print(f"\n🔍 Scraping Job Bank Canada (NOC {job_code})...")
        
        try:
            # Job Bank wage report URL
            url = f"https://www.jobbank.gc.ca/marketreport/wages-occupation/{job_code}/ca"
            
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract wage information
            wage_data = {}
            
            # Look for wage tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        key = cells[0].get_text(strip=True)
                        value = cells[1].get_text(strip=True)
                        wage_data[key] = value
            
            if wage_data:
                self.results.append({
                    'source': 'Job Bank Canada',
                    'job_title': f'NOC {job_code}',
                    'wage_data': json.dumps(wage_data),
                    'scraped_date': datetime.now().strftime('%Y-%m-%d')
                })
                print(f"  ✓ Collected wage data")
            else:
                print(f"  ⚠️  No wage data found")
                
            self.delay()
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    def scrape_with_selenium(self, url):
        """
        Example using Selenium for JavaScript-heavy sites
        Uncomment and use when needed
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from webdriver_manager.chrome import ChromeDriverManager
            
            print("\n🔍 Using Selenium for dynamic content...")
            
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
            
            time.sleep(3)  # Wait for JavaScript to load
            
            # Extract data using Selenium
            # Example: elements = driver.find_elements(By.CLASS_NAME, 'salary-info')
            
            driver.quit()
            print("  ✓ Selenium scraping completed")
            
        except ImportError:
            print("  ℹ️  Selenium not installed. Run: pip install selenium webdriver-manager")
        except Exception as e:
            print(f"  ✗ Selenium error: {e}")
    
    def save_results(self, filename='stat_real_data_scraped.csv'):
        """Save scraped data to CSV in real_data folder"""
        if not self.results:
            print("\n⚠️  No data collected to save")
            return None
        
        output_path = self.output_dir / filename
        df = pd.DataFrame(self.results)
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✅ Saved {len(self.results)} records to {output_path}")
        
        # Display summary
        print("\n📊 Data Summary:")
        print(df.head(10))
        
        return df
    
    def export_to_json(self, filename='stat_real_data_scraped.json'):
        """Export results to JSON format"""
        if not self.results:
            print("\n⚠️  No data to export")
            return
        
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported to {output_path}")


def main():
    """Main execution function"""
    print("="*60)
    print("AI Salary Data Scraper for Canada")
    print("="*60)
    
    scraper = AISalaryScraper(output_dir='data/real_data')
    
    # Example 1: Scrape Indeed for AI Engineer positions
    scraper.scrape_indeed_ca(job_title="AI Engineer", location="Toronto, ON", max_pages=2)
    
    # Example 2: Scrape Indeed for Data Scientist positions
    scraper.scrape_indeed_ca(job_title="Data Scientist", location="Vancouver, BC", max_pages=2)
    
    # Example 3: Scrape Indeed for Machine Learning positions
    scraper.scrape_indeed_ca(job_title="Machine Learning Engineer", location="Montreal, QC", max_pages=2)
    
    # Example 4: Get data from Job Bank Canada
    scraper.scrape_job_bank_ca(job_code="21211")  # Data Scientists
    scraper.scrape_job_bank_ca(job_code="21231")  # Software Engineers
    
    # Save results
    df = scraper.save_results('stat_real_data_scraped_jobs.csv')
    scraper.export_to_json('stat_real_data_scraped_jobs.json')
    
    print("\n" + "="*60)
    print("✅ Scraping Complete!")
    print("="*60)
    
    return df


if __name__ == "__main__":
    # Run the scraper
    data = main()
    
    # Additional analysis
    if data is not None and not data.empty:
        print("\n📈 Quick Analysis:")
        print(f"Total jobs found: {len(data)}")
        print(f"\nJobs by source:")
        print(data['source'].value_counts())
        
        # Filter jobs with salary info
        jobs_with_salary = data[data['salary'] != 'Not Listed']
        print(f"\nJobs with salary information: {len(jobs_with_salary)}")
