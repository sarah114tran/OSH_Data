{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "f9d6c75c-1671-4a67-9ae0-cffb0adfd696",
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "import json\n",
    "import pandas as pd\n",
    "from pandas import json_normalize"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "635d1e3a-92ca-4a4d-959a-f3e95ff0ce96",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Scraped 564 repositories from Open Hardware Repository.\n"
     ]
    }
   ],
   "source": [
    "BASE_URL = \"https://ohwr.org/api/v4/projects\"\n",
    "params = {\n",
    "    \"per_page\": 100,\n",
    "    \"page\": 1\n",
    "}\n",
    "\n",
    "all_repos = []\n",
    "\n",
    "while True:\n",
    "    response = requests.get(BASE_URL, params=params)\n",
    "    if response.status_code != 200:\n",
    "        break\n",
    "    \n",
    "    data = response.json()\n",
    "    if not data:\n",
    "        break\n",
    "    \n",
    "    all_repos.extend(data)\n",
    "    params[\"page\"] += 1  # Move to next page\n",
    "\n",
    "# Save as JSON\n",
    "with open(\"OHR_repos.json\", \"w\") as f:\n",
    "    json.dump(all_repos, f, indent=4)\n",
    "\n",
    "print(f\"Scraped {len(all_repos)} repositories from Open Hardware Repository.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "440ae483-1a97-4748-a564-53d7856ed266",
   "metadata": {},
   "outputs": [],
   "source": [
    "with open(\"OHR_repos.json\") as open_file:\n",
    "    data = json.load(open_file)\n",
    "\n",
    "data = [item for sublist in data for item in sublist]\n",
    "\n",
    "df = pd.DataFrame(data)\n",
    "\n",
    "df.to_csv(\"OHR_repos.csv\", index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "9140c3aa-1166-4b88-a695-0bc2aa3d6259",
   "metadata": {},
   "outputs": [],
   "source": [
    "def flatten_json(json_data):\n",
    "    flattened_data = json_normalize(json_data)\n",
    "    return flattened_data\n",
    "\n",
    "def json_to_csv(json_file, csv_file):\n",
    "    # Read JSON file\n",
    "    with open(json_file, 'r') as f:\n",
    "        json_data = json.load(f)\n",
    "\n",
    "    # Flatten JSON data\n",
    "    flattened_data = flatten_json(json_data)\n",
    "    \n",
    "    # Write flattened data to CSV\n",
    "    flattened_data.to_csv(csv_file, index=False)\n",
    "\n",
    "# Example usage\n",
    "json_file = 'OHR_repos.json'\n",
    "csv_file = 'OHR_repos.csv'\n",
    "json_to_csv(json_file, csv_file)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
