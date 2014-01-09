#!/usr/bin/env ruby
#
# Copyright (C) 2014 Eric DePree
#
# This quiz is free software; you can redistribute it and/or modify
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
# Copyright::  Copyright (c) 2014
# License::    GPLv2

require "optparse"

OPTIONS = Hash.new

NUMBERS = {"1" => [],
           "2" => ["a", "b", "c"],
           "3" => ["d", "e", "f"],
           "4" => ["g", "h", "i"],
           "5" => ["j", "k", "l"],
           "6" => ["m", "n", "o"],
           "7" => ["p", "q", "r", "s"],
           "8" => ["t", "u", "v"],
           "9" => ["w", "x", "y", "z"],
           "0" => []}

# --------------------
# Read in and validate mandatory command line arguments.
# --------------------
def read_arguments()
    OptionParser.new do |opts|
        opts.banner = "Usage: quiz.rb [OPTIONS]"

        opts.on("-i", "--input NUMBER", "Phone Number") do |input_numbers|
            OPTIONS[:numbers] = input_numbers
        end

        opts.on("-w", "--word_list PATH", "File path to a word list") do |word_list_path|
            options[:word_list] = word_list_path
        end
    end.parse!

    # Validate mandatory input is specified
    if OPTIONS[:numbers] == nil
        puts "No phone number specified"
        exit
    end

    # Populate optional arguments
    if OPTIONS[:word_list] == nil
        OPTIONS[:word_list] = "/usr/share/dict/words"
    end
end

def load_wordlist(file_path)
    file_buffer = Array.new

    if !File.exists?(file_path)
        puts "File '#{file_path}' does not exits."
        exit
    end

    File.open(file_path, "r").each_line do |line|
        if line.length < 8
            file_buffer << line
        end
    end

    file_buffer.map!{ |line| line.downcase.chomp }

    return file_buffer
end

# --------------------
# Strip input phone number into base format.
# Generate a list of all possible strings from phone number.
# --------------------
def generate_string_combinations(phone_number)
    word_array = Array.new

    phone_number = phone_number.gsub(/[.-]/, '')
    phone_number.strip!

    phone_number.each_char do |i|
        word_array << NUMBERS[i]
    end

    transformed_array = word_array.first.product(*word_array[1..-1]).map(&:join)

    return transformed_array
end

# --------------------
#
# --------------------
def generate_words(unused_characters)
    # Complete word found
    if unused_characters.length == 0
        return true
    end

    i = 0

    while i < unused_characters.length do

        possible_word = unused_characters[0..i]

        if possible_word.length > 2

            if WORDLIST.include? possible_word

                if possible_word.length == 7
                    puts "#{possible_word}"
                end

                found_word = generate_words(unused_characters[(i+1)..(unused_characters.length)])

                if found_word
                    return true
                end
            end
        end

        i += 1
    end

    return false
end

# --------------------
# Program Flow
# --------------------
read_arguments()
WORDLIST = load_wordlist(OPTIONS[:word_list])

generate_string_combinations(OPTIONS[:numbers]).each do |possible_word|
    if generate_words(possible_word)
        puts possible_word
    end
end