set -x

day=$(date "+%-d")
year=$(date "+%Y")
day=22
year=2019
puzzle_url="https://adventofcode.com/${year}/day/${day}"
input_url="https://adventofcode.com/${year}/day/${day}/input"
input_file="day${day}_input.txt"
script_file="day${day}.py"

# Open pages
firefox "${puzzle_url}"
firefox "${input_url}"

# Create empty input file
touch "${input_file}"

# Create script file based on template
cp ./day_template.py "${script_file}"
sed -i "s/DAYNUMBER/${day}/g" "${script_file}"

# Add line to README.md
echo -e "\n${puzzle_url} : 0/2" >> README.md

# Change number of days in all_days.py
sed -i "s/^\(nb_days = \).*/\1${day}/g" all_days.py

# Add everything and commit
git add "${input_file}" "${script_file}" README.md
git commit -m "Day ${day} - part 1"

# Open relevant files to start solving the problem
vim "${script_file}" "${input_file}"
