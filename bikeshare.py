from PyInquirer import prompt, print_json
import calendar as cal #Used calender for better Readbility of user's outputs (e.g. getting month name instead of a number)
import time
import pandas as pd
import numpy as np



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #### Using PyInquirer to have a fancy user interaction instead of bothering with typing :)
    #Getting City data
    questions = [
        {
            'type': 'list',
            'name': 'City',
            'message': 'Please Select one of the following cities:',
            'choices' : ['chicago','new york city','washington'],
        }
    ]

    answers = prompt(questions)
    city = answers.get("City","")

    #Getting Month
    questions = [
        {
            'type': 'list',
            'name': 'Month',
            'message': 'Please Select one of the following Months:',
            'choices' : ['all','january', 'february', 'march', 'april', 'may', 'june'],
        }
    ]

    answers = prompt(questions)
    month = answers.get("Month","")

    #Getting Day
    questions = [
        {
            'type': 'list',
            'name': 'Day',
            'message': 'Please Select one of the following days',
            'choices' : ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday'],
        }
    ]

    answers = prompt(questions)
    day = answers.get("Day","")
    ####

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #city = input("\nPlease Type one of the following Cities [chicago, new york city, washington]: ")
    #city = city.lower()
    while city not in CITY_DATA.keys():
        city = input("The vlaue you've entered isn't of the list given [chicago, new york city, washington]. Please enter the city name again: ").lower()

    # get user input for month (all, january, february, ... , june)
    #List for condition check
    months = ['january', 'february', 'march', 'april', 'may', 'june','all']
    #month = input("Please type the month name or [all]: ").lower().strip(' ')

    while month not in months :    
        month = input("Wrong Value!\n please type 1 of the following (all, january, february, ... , june): ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday','all']
    #day = input("Please type the day of week name or [all]: ")
    while day not in days :    
        day = input("Wrong Value!\n please type 1 of the following: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Referenceing solved Quiz 3 code in UDACITY (My Solution):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    

    # extract month and day_of_week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 #+1 because iteration starts from 0 not 1.
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = cal.month_name[df['month'].mode()[0]] #Used Calender lib to output month name
    
        

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]


    # display the most common start hour
    most_common_start_time = df['Start Time'].dt.hour.mode()[0]   


    print("Most frequent month is: ", most_common_month)
    print("Most frequent day is: ", most_common_day)
    print("Most frequent Starting Hour is: ", most_common_start_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0] 
    
    # display most frequent combination of start station and end station trip and thier Count
    most_common_combo_station = df.groupby(['Start Station','End Station']).count().sort_values(['Start Time'], ascending=False).head(1)
    most_common_combo_station = most_common_combo_station.iloc[:,0:1]
    most_common_combo_station.columns = ['Count']
    
    print("Most Frequent Starting Station is: ", most_common_start_station)
    print("Most Frequent Ending Station is: ", most_common_end_station)
    print("Most frequent of combination of Starting and Ending Trip is: \n", most_common_combo_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].describe()[4]
    #or# mean_travel_time = df['Trip Duration'].mean(axis = 0)

    print('Total Travel Time:',total_travel_time,'Seconds')
    print('Mean Travel Time:',mean_travel_time,'Seconds')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].nunique()

    # Display counts of gender
    count_Gender = df['Gender'].nunique()

    # Display earliest, most recent, and most common year of birth
    #check if column exists in the DataFrame; one city doesn't have that.
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].describe()[6] 
        most_recent_birth_year = df['Birth Year'].describe()[-1] 
        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
    else:
        print("The city you've selected doesn't contain Year of Birth Information") 

    print('Count of User Types:',count_user_type,'Type(s)')
    print('Count of Genders:',count_Gender,'Gender(s)')
    print('Earlist birth year:',earliest_birth_year,'\nMost recent birth year',most_recent_birth_year,'\nMost common birth year:',most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
  
        #restart = input('\nWould you like to restart? Enter yes or no.\n')
        #Alternative script Restart Selction Yes/No/Display raw data
        questions = [
            {
                'type': 'list',
                'name': 'choice',
                'message': 'Would you like to restart?',
                'choices' : ['Yes','No','display some raw data'],
            }
        ]
        
        answers = prompt(questions)
        restart = answers.get("choice","")
        if restart.lower() == 'no':
            break
        ###Display 5 raw data at a time (Based on User's Selection & Filters selected)
        elif restart.lower() == 'display some raw data':
            raw_data_flag = True
            start_index = 0 
            end_inedx = 5
            while raw_data_flag == True :
                print(df[start_index:end_inedx])

                questions = [
                    {
                        'type': 'list',
                        'name': 'choice',
                        'message': 'Do you want to Display more data?',
                        'choices' : ['Yes','No'],
                    }
                ]
                answers = prompt(questions)
                restart = answers.get("choice","")
                if restart.lower() == 'no':
                    raw_data_flag = False
                start_index += 5
                end_inedx += 5
            print('Happy Data Analysing! Good Bye :)')
            break
        ###     
        


if __name__ == "__main__":
	main()
