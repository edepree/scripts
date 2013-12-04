#!/usr/bin/env ruby
#
# Copyright (C) 2013 Eric DePree
#
# This decoder_ring is free software; you can redistribute it and/or modify
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

require 'stringio'
require 'optparse'

=begin
    Read in a file from disk, save it into a list and return it.
    Exit the application with an error message if the file doesn't exits.
=end
def read_in_file(file_path)
    file_buffer = []

    if !File.exists?(file_path)
        puts "File '#{file_path}' does not exits."
        exit
    end

    File.open(file_path, "r").each_line do |line|
        file_buffer << line
    end

    return file_buffer
end

=begin
    Load a word list from disk, uppercase it, chomp it
    and return an array of words.
=end
def load_wordlist(file_path)
    wordlist = read_in_file(file_path)

    wordlist.map!{ |line| line.upcase.chomp }

    return wordlist
end

=begin
    Take a word list in and the encoded key. For every possible Caesar cipher
    shift the text, check it against the word list and return the results.
    If no match is found return nil.
=end
def decode_ceasar_cipher_key(wordlist, input_text)
    buffer = StringIO.new

    (1...26).step(1) do |shift|
        input_text.each_byte do |c|
            buffer << shift_character(c, shift, true)
        end

        if wordlist.include? buffer.string
            return buffer.string
        end

        buffer = StringIO.new
    end

    return nil
end

=begin
    Load in the encoded message and the key. Decipher it, put in into a buffer
    and return the plain text.
=end
def decode_vigenere_cipher(key, message)
    buffer = StringIO.new

    key_ascii_array = []
    key.each_char { |c| key_ascii_array << (c.ord - 65) }

    i = 2
    current_key_position = 0

    while i < message.size do
        current_line = message[i]

        current_line.each_byte do |c|
            if valid_character?(c)
                transformed_character = shift_character(c, key_ascii_array[current_key_position], false)

                current_key_position = (current_key_position + 1 < key.size) ? (current_key_position + 1) : 0

                buffer << transformed_character
            else
                buffer << c.chr
            end
        end

       i += 1
    end

    return buffer.string
end

=begin
    If a character is between 65 (A) and 91 (Z) then return true, otherwise
    return false.
=end
def valid_character?(character)
    return (character >= 65 && character <= 90)
end

=begin
    Shift an capitalized ASCII character shifted the appropriate positive or
    negative amount.
=end
def shift_character(input_character, shift, positive_shift)

    if positive_shift
        return ((((input_character - 65) + shift) % 26) + 65).chr
    else
        return ((((input_character - 65) - shift) % 26) + 65).chr
    end
end

# Load options from the command line
options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: decoder_ring.rb [options]"

  opts.on("-c", "--cipher PATH", "File path to the cipher file") do |cipher_path|
    options[:cipher] = cipher_path
  end

  opts.on("-w", "--word_list PATH", "File path to a word list") do |word_list_path|
    options[:word_list] = word_list_path
  end
end.parse!

# Validate mandatory input is specified
if options[:cipher] == nil
    puts "No cipher file specified"
    exit
end

if options[:word_list] == nil
    puts "No word list file specified"
    exit
end

# Read in word list
wordlist = load_wordlist(options[:word_list])

# Read in cipher file
encoded_file = read_in_file(options[:cipher])
encoded_key = encoded_file.first.chomp

# Find Caesar cipher of key
decoded_key = decode_ceasar_cipher_key(wordlist, encoded_key)

if decoded_key == nil
    puts "No Key Found!"
    exit
end

puts "Your Key Is: #{decoded_key}"

#Decode message
decoded_message = decode_vigenere_cipher(decoded_key, encoded_file)

puts "Your Message Is: #{decoded_message}"