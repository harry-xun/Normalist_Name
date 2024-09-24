import unittest
from api import NamesAPI

class TestNamesApi(unittest.TestCase):
    def setUp(self):
        self.fb = NamesAPI()


    def test_get_popularity_of_existing_name(self):
        name = "Robert"
        year = 2000
        self.assertEqual(self.fb.get_popularity_of(name, year), 13762)

    def test_get_popularity_of_name_from_1700(self):
        name = "Robert"
        year = 1700
        self.assertEqual(self.fb.get_popularity_of(name, year), -1)

    def test_get_popularity_of_non_existing_name(self):
        name = "Harricane"
        year = 2000
        self.assertEqual(self.fb.get_popularity_of(name, year), -1)

    def test_generate_name_from(self):
        lower_bound_year = 2008
        upper_bound_year = 2010
        lower_bound_popularity = 3995
        upper_bound_popularity = 4000

        self.assertEqual(self.fb.generate_name_from(lower_bound_year,upper_bound_year,lower_bound_popularity,upper_bound_popularity), [('Zoey',)])
    
    def test_generate_name_from_no_year(self):
        lower_bound_year = 1600
        upper_bound_year = 2010
        lower_bound_popularity = 9600
        upper_bound_popularity = 9900

        self.assertEqual(self.fb.generate_name_from(lower_bound_year,upper_bound_year,lower_bound_popularity,upper_bound_popularity), -1)

    def test_generate_name_from_no_year_interval(self):
        lower_bound_year = 2012
        upper_bound_year = 2010
        lower_bound_popularity = 9600
        upper_bound_popularity = 9900

        self.assertEqual(self.fb.generate_name_from(lower_bound_year,upper_bound_year,lower_bound_popularity,upper_bound_popularity), [])

    def test_generate_name_from_no_popularity_interval(self):
        lower_bound_year = 2001
        upper_bound_year = 2010
        lower_bound_popularity = 10000
        upper_bound_popularity = 9900

        self.assertEqual(self.fb.generate_name_from(lower_bound_year,upper_bound_year,lower_bound_popularity,upper_bound_popularity), -1)

    def test_generate_name_from_negative_input(self):
        lower_bound_year = 2012
        upper_bound_year = 2010
        lower_bound_popularity = -100
        upper_bound_popularity = 9900

        self.assertEqual(self.fb.generate_name_from(lower_bound_year,upper_bound_year,lower_bound_popularity,upper_bound_popularity), -1)
    
    
    def test_Name_Sex_Distribution(self):
        name = "Kelly"
        year= 2015

        self.assertEqual(self.fb.get_sex_ratio(name,year),0.13367609254498714)

    def test_Name_Sex_Distribution_Wrong_Year(self):
        name = "Kelly"
        year= 1715

        self.assertEqual(self.fb.get_sex_ratio(name,year),-1)

    def test_Name_Sex_Distribution_No_Name(self):
        name = "Helli"
        year= 1915

        self.assertEqual(self.fb.get_sex_ratio(name,year),-1)

    def test_Get_Names(self):
        name = "luke"

        self.assertEqual(self.fb.generate_name_from_partial(name),['Luke', 'Lukeanthony', 'Luken', 'Lukes', 'Lukesha', 'Lukeshia', 'Lukeus'])

    def test_Cant_Get_Names(self):
        name = "lukey"

        self.assertEqual(self.fb.generate_name_from_partial(name),[])

    def test_Get_Most_Used_Year_Of(self):
        name = 'Doug'
        
        self.assertEqual(self.fb.Get_Most_Used_Year_Of(name),1962)

    def test_Get_Most_Used_Year_Of_Wrong_Name(self):
        name = 'Douggeorge'
        
        self.assertEqual(self.fb.Get_Most_Used_Year_Of(name),-1)

if __name__ == "__main__":
    unittest.main()
