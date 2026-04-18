#include <string>
#include <set>
#include <vector>
#include <random>
#include <utility>
#include <fstream>
#include <functional>
#include <iostream>

//~ std::vector<int> length_string_v{4, 10};
//~ const int max_number_strings = 40;
//~ const int step_size = max_number_strings / 10;
std::vector<int> length_string_v{10, 50, 100, 500};
const int max_number_strings = 1e6;
const int step_size = max_number_strings / 100;

// Functions from: https://www.partow.net/programming/hashfunctions/index.html
// 00 - RS Hash Function
unsigned int RSHash(const std::string& str)
{
   unsigned int b    = 378551;
   unsigned int a    = 63689;
   unsigned int hash = 0;

   for (char c : str)
   {
      hash = hash * a + c;
      a    = a * b;
   }

   return hash;
}

// 01 - JS Hash Function
unsigned int JSHash(const std::string& str)
{
   unsigned int hash = 1315423911;

   for (char c : str)
   {
      hash ^= ((hash << 5) + c + (hash >> 2));
   }

   return hash;
}

// 02 - PJW Hash Function
unsigned int PJWHash(const std::string& str)
{
   const unsigned int BitsInUnsignedInt = (unsigned int)(sizeof(unsigned int) * 8);
   const unsigned int ThreeQuarters     = (unsigned int)((BitsInUnsignedInt  * 3) / 4);
   const unsigned int OneEighth         = (unsigned int)(BitsInUnsignedInt / 8);
   const unsigned int HighBits          = (unsigned int)(0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth);
   unsigned int hash = 0;
   unsigned int test = 0;

   for (char c : str)
   {
      hash = (hash << OneEighth) + c;

      if ((test = hash & HighBits) != 0)
      {
         hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits));
      }
   }

   return hash;
}

// 03 - ELF Hash Function
unsigned int ELFHash(const std::string& str)
{
   unsigned int hash = 0;
   unsigned int x    = 0;

   for (char c : str)
   {
      hash = (hash << 4) + c;

      if ((x = hash & 0xF0000000L) != 0)
      {
         hash ^= (x >> 24);
      }

      hash &= ~x;
   }

   return hash;
}

// 04 - BKDR Hash Function
unsigned int BKDRHash(const std::string& str)
{
   unsigned int seed = 131; /* 31 131 1313 13131 131313 etc.. */
   unsigned int hash = 0;

   for (char c : str)
   {
      hash = (hash * seed) + c;
   }

   return hash;
}

// 05 - SDBM Hash Function
unsigned int SDBMHash(const std::string& str)
{
   unsigned int hash = 0;

   for (char c : str)
   {
      hash = c + (hash << 6) + (hash << 16) - hash;
   }

   return hash;
}

// 06 - DJB Hash Function
unsigned int DJBHash(const std::string& str)
{
   unsigned int hash = 5381;

   for (char c : str)
   {
      hash = ((hash << 5) + hash) + c;
   }

   return hash;
}

// 07 - DEK Hash Function
unsigned int DEKHash(const std::string& str)
{
   unsigned int hash = str.length();

   for (char c : str)
   {
      hash = ((hash << 5) ^ (hash >> 27)) ^ c;
   }

   return hash;
}

// 08 - AP Hash Function
unsigned int APHash(const std::string& str)
{
   unsigned int hash = 0xAAAAAAAA;
   unsigned int i    = 0;

   for (char c : str)
   {
      hash ^= ((i & 1) == 0) ? (  (hash <<  7) ^ c * (hash >> 3)) :
                               (~((hash << 11) + (c ^ (hash >> 5))));
      ++i;
   }

   return hash;
}

const std::vector<
	std::pair<
		std::string, std::function<unsigned int(const std::string&)>
	>
> hash_name_and_function_v
{
	{"RS", RSHash},
	{"JS", JSHash},
	{"PJW", PJWHash},
	{"ELF", ELFHash},
	{"BKDR", BKDRHash},
	{"SDBM", SDBMHash},
	{"DJB", DJBHash},
	{"DEK", DEKHash},
	{"AP", APHash}
};

struct Result
{
	int length_string;
	std::string hash_name;
	int number_strings;
	int number_collisions;
};

int random_char()
{
	static std::random_device rd;
    static std::mt19937 gen(rd());
    
    static std::uniform_int_distribution<> dis('a', 'z');
    return dis(gen);
}

std::vector<std::string> generate_strings(const int length_string)
{
	std::set<std::string> set_strings;
	std::vector<std::string> v;
	while(v.size() < max_number_strings)
	{
		std::string s(length_string, '_');
		for(auto& c: s)
		{
			c = random_char();
		}
		
		if((set_strings.insert(s)).second)
		{
			v.push_back(s);
		}
	}
	
	//~ for(auto s: v)
	//~ {
		//~ std::cout << s << '\n';
	//~ }
	//~ std::cout << std::endl;
	
	//~ v[13] = v[2];
	//~ v[22] = v[2];
	std::cout << "String generation complete, n=" << max_number_strings << " l=" << length_string << std::endl;
	return v;
}

std::vector<Result> result_for_fixed_length(const int length_string)
{
	
	std::vector<Result> results;
	
	for(const auto& [hash_name_str, hash_function]: hash_name_and_function_v)
	{
		auto strings_v = generate_strings(length_string);
		
		std::set<unsigned int> hash_set;
		
		Result result;
		result.length_string = length_string;
		result.hash_name = hash_name_str;
		result.number_strings = 0;
		result.number_collisions = 0;
		
		for(int i = 0; i < max_number_strings; ++ i)
		{
			const auto& s = strings_v[i];
			auto hash_value = hash_function(s);
			
			result.number_collisions += (!((hash_set.insert(hash_value)).second));
			result.number_strings = i + 1;
			
			if(result.number_strings % step_size == 0)
			{
				results.push_back(result);
			}
		}
	}		
	
	return results;
}

void save_to_file(const std::vector<Result>& results)
{
	std::ofstream fout("data.txt");
	
	fout << "length_string\thash_name\tnumber_strings\tcollision_proportion" << "\n";
	
	for(const auto& result: results)
	{
		double proportion_collisions = result.number_collisions;
		proportion_collisions /= result.number_strings;
		fout << result.length_string << "\t" << result.hash_name << "\t" << result.number_strings << "\t" << proportion_collisions << "\n";
	}
}

void run_experiment()
{
	
	std::vector<Result> results;
	for(int length_string: length_string_v)
	{
		std::cout << "\n" << "Running program for length_string=" << length_string << std::endl;
		
		auto result = result_for_fixed_length(length_string);
		
		results.insert(results.end(), result.begin(), result.end());
	}
	
	save_to_file(results);
}

	
int main()
{
	run_experiment();
	std::cout << "Experiment complete" << std::endl;	
	return 0;
}
