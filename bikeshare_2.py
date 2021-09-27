import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Created lists for city, month and day for ease of modifying

city_value = ['chicago','new york','washington']
month_value = ['january', 'february', 'march', 'april', 'may', 'june','all']
day_value = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

              
def get_filters():
    """Print instructions for user to provide filters"""
    
    print('\nHello! Let\'s explore some US bikeshare data!')
    #Collect and validate user input for city (chicago, new york city, washington)
    while True:
        print('\nPlease choose a city from: ', city_value)
        user_input=input().lower()
        if user_input in city_value:
            city = user_input
            print('Selected city is: ', city.title())
            break
        else:
            print('Invalid Input, please re-enter input')
    
    #Collect and validate user input for month (all, january, february, ... , june)
    while True:
        print('\nPlease choose a month from: ', month_value)
        user_input=input().lower()
        if user_input in month_value:
            month = user_input
            print('Selected month is: ', month.title())
            break
        else:
            print('Invalid Input, please re-enter input')
    
    #Collect and validate user input for day of week (all, monday, tuesday, ... sunday) 
    while True:
        print('\nPlease choose a day from: ', day_value)
        user_input=input().lower()
        if user_input in day_value:
            day = user_input
            print('Selected day is: ', day.title())
            break
        else:
            print('Invalid Input, please re-enter input')
   
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
    
    print('\nData Load in progess...')
    df = pd.read_csv(CITY_DATA[city])
    print('\nData Load Successfull!!')
    
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day'] = pd.to_datetime(df['Start Time']).dt.day_name()
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    
    #Filter by month logic, converting to month number
    if month != 'all':
        month = month_value.index(month) + 1

        #Filtering by user input month index
        df = df[df['month'] == month]

    #Filtering by user input day
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]


    return df


def time_stats(df):
   """Displays statistics on the most frequent times of travel."""
   
   print('\nCalculating The Most Frequent Times of Travel...')
   start_time = time.time()

   # display the most common month
   common_month = df['month'].mode()[0]
   print('\nThe most common Month is: ', common_month)

   # display the most common day of week
   common_day = df['day'].mode()[0]
   print('\nThe most common Day Of Week is: ', common_day.title())

   # display the most common start hour
   common_start_hour = df['hour'].mode()[0]
   print('\nThe most common Start Hour is: ', common_start_hour)


   print("\nThis took %s seconds." % (time.time() - start_time))
   print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is: ', common_start_station.title())

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe most common End Station is: ', common_end_station.title())

    # display most frequent combination of start station and end station trip
    df['Combo Station'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')
    combo_station = df['Combo Station'].mode()[0]
    
    print('\nThe most frequent combination of Start Station and End Station is:\n', combo_station.title())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration"""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nthe total travel time is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users"""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print('\nCount of User Type: ')
    print(df['User Type'].value_counts())
    
    if city == 'washington':
        print('\nUser stats not available for selected city')
    else:
        # Display counts of gender
        print('\nCount of Gender: ')
        print(df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('\nThe earliest birth year is: ',earliest_year)
        most_recent_year = df['Birth Year'].max()
        print('\nThe most recent birth year is: ',most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('\nThe most common birth year is: ',most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 rows of data upon request by the user"""
    
    choice = 'y'
    counter = 0
    
    while choice == 'y':
        print('\nDo you wish to view 5 rows of raw data?y/n')
        choice = input().lower()
        if choice == 'y':
            print(df[counter:counter+5])
            counter += 5
        elif choice == 'n':
            break            
        else:
            print('Invalid Input, please re-enter input as requested')
            choice = 'y'
            
    print('-'*40)

def main():
    restart = 'y'
    while restart == 'y':
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? y/n\n').lower()
        
        while restart.lower() != 'y' and restart.lower() != 'n':
            print('Invalid Input, please re-enter input as requested')
            restart = input('\nWould you like to restart? y/n\n').lower()
        
        
if __name__ == "__main__":
	main()
