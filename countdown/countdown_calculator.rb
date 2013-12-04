#!/usr/bin/env ruby
#
# Copyright (C) 2013 Eric DePree
#
# This countdown_calculator is free software; you can redistribute it and/or modify
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
# Author::     Eric DePree, Nate Nelles
# Copyright::  Copyright (c) 2013
# License::    GPLv2

require "optparse"

OPTIONS = Hash.new
MULTIPLICATION_NUMBERS = Array.new()

numbers_list = Array.new()
target_number = 0

modified_target_number = 0
numbers_list_working_set = Array.new()

# --------------------
# Read in and validate mandatory command line arguments.
# --------------------
def read_arguments()
    OptionParser.new do |opts|
        opts.banner = "Usage: countdown_calculator.rb [OPTIONS]"

        opts.on("-i", "--input NUMBERS", "Input Numbers") do |input_numbers|
            OPTIONS[:numbers] = input_numbers
        end
    end.parse!

    # Validate mandatory input is specified
    if OPTIONS[:numbers] == nil
        puts "No numbers specified"
        exit
    end
end

def print_inputs()
    numbers_list = OPTIONS[:numbers].split(",").map! {|i| i.to_f}
    target_number = rand(100 .. 999).to_f

    puts "Your input numbers are #{numbers_list}"
    puts "Your target number is #{target_number}"

    return numbers_list, target_number
end

def do_math_high_number(numbers_list, target_number)
    highest_number = numbers_list.max.to_f
    higest_number_quotient = (target_number / highest_number)

    puts "Highest Number Is #{highest_number}"
    puts "Higest Number Quotient Is #{higest_number_quotient}"

    numbers_list_working_set = numbers_list

    numbers_list_working_set.delete(numbers_list_working_set.max)
    working_set_weights = numbers_list_working_set.map {|i| (i.to_f - higest_number_quotient).abs}

    lowest_weight_index = working_set_weights.each_with_index.min[1]
    lowest_weight_number = numbers_list_working_set[lowest_weight_index]

    puts "Working Set #{numbers_list_working_set}"
    puts "Working Set Weights #{working_set_weights}"
    puts "Lowest Weight Number #{lowest_weight_number}"

    MULTIPLICATION_NUMBERS << lowest_weight_number
    numbers_list_working_set.delete(lowest_weight_number)

    modified_target_number = target_number - (highest_number * lowest_weight_number)

    return numbers_list_working_set, modified_target_number
end

def remove_numbers_from_array(index, number_list)

    puts "Index is #{index}"
    puts "Number List #{number_list}"

    if index != 0.0
        if index.odd?
            puts "Removing #{number_list[index]}"
            number_list.delete_at(index)
            puts "Removing #{number_list[index]}"
            number_list.delete_at(index)
        else
            number_list.delete_at(index-1)
            number_list.delete_at(index-1)
        end
    end

    return number_list
end

def brute_force(numbers_list, target_number)

    if target_number == 0
        return
    end
    working_set = numbers_list
    working_set << working_set.clone
    working_set << 0.0
    working_set.flatten!.sort!

    temp_array = Array.new()
    odd_number = false

    for number in working_set
        if odd_number
            temp_array << number * -1.0
            odd_number = false
        else
            temp_array << number
            odd_number = true
        end
    end

    working_set = temp_array


    puts "Modified Working Set #{working_set}"

    for a in 0..8
        working_set_two = working_set.clone

        a_number = working_set_two[a]
        working_set_two = remove_numbers_from_array(a, working_set_two)

        for b in 0..(working_set_two.length-1)
            b_number = working_set_two[b]
            working_set_two = remove_numbers_from_array(b, working_set_two)

            for c in 0..(working_set_two.length-1)
                c_number = working_set_two[c]
                working_set_two = remove_numbers_from_array(c, working_set_two)

                for d in 0..(working_set_two.length-1)
                    d_number = working_set_two[d]
                    working_set_two = remove_numbers_from_array(d, working_set_two)

                    puts "A: #{a_number} B: #{b_number} C: #{c_number} D: #{d_number}"
                end
            end
        end
    end
end

read_arguments()
numbers_list, target_number = print_inputs()
numbers_list_working_set, modified_target_number = do_math_high_number(numbers_list, target_number)
brute_force(numbers_list_working_set, modified_target_number)