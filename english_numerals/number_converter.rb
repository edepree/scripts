#!/usr/bin/env ruby
#
# Copyright (C) 2013 Eric DePree
#
# This number_converter is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Author::     Eric DePree
# Copyright::  Copyright (c) 2013
# License::    GPLv2

require "optparse"

OPTIONS = Hash.new

HUNDREDS_DIGIT = ["thousand", "million", "billion", "trillion"]

SINGLE_DIGIT = {"1" => "one",
                "2" => "two",
                "3" => "three",
                "4" => "four",
                "5" => "five",
                "6" => "six",
                "7" => "seven",
                "8" => "eight",
                "9" => "nine",
                "0" => "zero"}

TENS_DIGIT = {"1" => "ten",
              "2" => "twenty",
              "3" => "thirty",
              "4" => "forty",
              "5" => "fifty",
              "6" => "sixty",
              "7" => "seventy",
              "8" => "eighty",
              "9" => "ninety",
              "0" => ""}

SPECIAL_DIGIT = {"11" => "eleven",
                  "12" => "twelve",
                  "13" => "thirteen",
                  "14" => "fourteen",
                  "15" => "fifteen",
                  "16" => "sixteen",
                  "17" => "seventeen",
                  "18" => "eighteen",
                  "19" => "nineteen"}

# --------------------
# Convert a numeric period into its English representation.
# --------------------
def build_english_number(input_period)
    output_buffer = String.new
    special_digits_regex = /^\d*1[1-9]$/
    input_character_location = ((input_period.length - 1) % 3)

    # String is solely a special value so output should be short circuited.
    if input_period.length == 2 and input_period.match(special_digits_regex)
        output_buffer << SPECIAL_DIGIT[input_period]
        return output_buffer
    end

    input_period.each_char do |input_character|
        case input_character_location
            when 0
                output_buffer << SINGLE_DIGIT[input_character]
            when 1
                output_buffer << TENS_DIGIT[input_character]
                input_character_location -= 1
            when 2
                output_buffer << SINGLE_DIGIT[input_character] << " hundred"
                input_character_location -= 1
        end

        output_buffer << " "

        # Remaining string is a special value so output should be short circuited.
        if input_period.length == 3 and input_period.match(special_digits_regex)
            output_buffer << SPECIAL_DIGIT[input_period[1,2]] << " "
            return output_buffer
        end
    end

    return output_buffer
end

# --------------------
# Parse the number entered by the user into an array of periods.
# --------------------
def build_period_list(number)
    period_list = Array.new
    current_lenght = number.length

    while current_lenght != 0
        if current_lenght <= 3
            period_list << number[0, current_lenght]
            current_lenght = 0
        else
            period_list << number[current_lenght-3, 3]
            current_lenght -= 3
        end
    end

    return period_list.reverse!
end

# --------------------
# Loop though each period extracted from the input number, convert each period
# to its English representation and build the entire English number into a string.
# --------------------
def build_entire_english_number(period_list)
    output_buffer = String.new
    hundreds_digit_position = (period_list.length - 2)

    period_list.each_with_index do |period, index|
        output_buffer << build_english_number(period)

        if index != (period_list.size - 1)
            output_buffer << HUNDREDS_DIGIT[hundreds_digit_position] << " "
        end

        hundreds_digit_position -= 1
    end

    return output_buffer
end

# --------------------
# Read in and validate mandatory command line arguments.
# --------------------
def read_arguments()
    OptionParser.new do |opts|
        opts.banner = "Usage: number_converter.rb [OPTIONS]"

        opts.on("-a", "--arabic NUMBER", "Arabic numeral") do |arabic_numeral|
            OPTIONS[:number] = arabic_numeral
        end
    end.parse!

    # Validate mandatory input is specified
    if OPTIONS[:number] == nil
        puts "No Arabic numeral specified"
        exit
    end
end

# --------------------
# "Main Method"
# --------------------
read_arguments()
period_list = build_period_list(OPTIONS[:number])
number_string = build_entire_english_number(period_list)
number_string.capitalize!

puts "Your number in English is: #{number_string}"