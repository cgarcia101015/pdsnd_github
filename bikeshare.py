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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please input city: ").lower()
    month = input("Please input month: ").lower()
    day = input("Please input day: ").lower()

    while city not in ['chicago','new york city','washington']:
        city = input("Invalid city! Please input city name: ").lower()

    while month not in ['all','january','february','march','april','may','june']:
        month = input("Invalid month! Please input the correct month: ").lower()

    while day not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        day = input("Invalid day! Please input the correct day: ").lower()


    print('-'*40)
    print(city, month, day)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['week_day'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())



    if month != 'all':
        month_list = ["all","january","february","march","april","may","june"]
        month = month_list.index(month) + 1

        df = df.loc[df['month'] == month,:]

    if day != 'all':

        df = df.loc[df['week_day'] == day,:]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract day from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    # find the most popular month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start month:', popular_month)

    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract day from the Start Time column to create an day column
    df['day'] = df['Start Time'].dt.day
    # find the most popular day
    popular_day = df['day'].mode()[0]
    print('Most Popular Start Day:', popular_day)

    # display the most common start hour

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().head(1)
    max_station = most_common_start_station.max()


    print("Most Common Start Station: ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().head(1)
    max_end_station = most_common_end_station.max()


    print("Most Common End Station: ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combo = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).head(1)
    print("Most frequent combination of stat and end station: ", most_frequent_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print('Total tavel time: ',travel_time)


    # display mean travel time
    travel_time_avg = df['Trip Duration'].mean()
    print('Total tavel time: ',travel_time_avg)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types)

    if city != 'washington':
        # Display counts of gender
        gender = df['Gender'].value_counts()

        print(gender)

        # Display earliest, most recent, and most common year of birth

        # Displays earliest birth year
        earliestBirthYear = df['Birth Year'].min()

        print("Earliest Birth Year: ",  int(earliestBirthYear))

        # Displays most recent birth Year
        latestBirthYear = df['Birth Year'].max()

        print("Latest Birth Year: ",  int(latestBirthYear))

        #Displays most common birth Year
        mostCommonBirthYear = df['Birth Year'].value_counts().head(1)
        max_item = mostCommonBirthYear.max()

        print("Most Common Birth Year: ", mostCommonBirthYear)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        index = 0
        print(df.iloc[index:index+5])

        while True:
            response = input('display 5 more lines ?')

            if response in ["yes", "no"]:

                if response == "yes":
                    index += 5
                    print(df.iloc[index:index+5])
                else:
                    break
            else:
                print("please input yes or no")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
