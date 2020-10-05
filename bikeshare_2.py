import time
import pandas as pd
import numpy as np
import datetime as dt
import json

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    chosen_city = None
    city = ('chicago', 'new york city', 'washington')
    while chosen_city not in city:
        chosen_city = input("Would you like to see data for Chicago, New York City or Washington?\n").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    chosen_month = None
    month = ('all', 'january', 'february', 'march',
                    'april', 'may', 'june')
    while chosen_month not in month:
        chosen_month = input("\nWhich month would you like to filter? january, february, "          "march, april, may, june or all?\n").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    chosen_day = None
    day = ('all', 'sunday', 'monday', 'tuesday',
                  'wednesday', 'thursday', 'friday', 'saturday')
    while chosen_day not in day:
        chosen_day = input("\nWhich day would you like to filter? sunday, monday, tuesday"
                    "wednesday, thursday, friday, saturday or all? ").lower()

    print('-'*40)
    return chosen_city, chosen_month, chosen_day


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
    print(" Your choices: "
          "{}, {} and {}".format(city, month, day))
    print()

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

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
    popular_month = df['month'].mode()[0]
    print('Most common Month: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day of the week: ', popular_day)

    # find the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common Start Hour: ', popular_hour)
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most Commonly Used Start '
          'Station: ', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('Most Commonly Used End '
          'Station: ', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' - ' + df['End Station']
    print('Most Frequent Combination: ', df['route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total Travel Time: ', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Mean Travel Time: ', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User Type Stats: ')
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
        print("\nDistribution for Each Gender:")
        print(df['Gender'].value_counts())
    except KeyError:
        print("There is no user genders data for this city: {}"
              .format(city.title()))

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('\nEarliest Birth '
              'Year: ', int(df['Birth Year'].min()))
        print('Most Recent Birth '
              'Year: ', int(df['Birth Year'].max()))
        print('Most Common Birth '
              'Year: ', int(df['Birth Year'].mode()[0]))
    except:
        print("\nThere is no birth year data for this city: {}"
              .format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    row_number = 5
    choose = input('Would you like to see raw data? '
                     'Enter yes or no : ').lower()
    df['Start Time'] = df['Start Time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    while choose == 'yes':
        print(json.dumps(df.head(row_number).to_dict('index'), indent=1))
        choose = input('Would you like to see 5 more '
                         'raw data? Enter yes or no : ').lower()
        row_number += 5    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data(df)

            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
