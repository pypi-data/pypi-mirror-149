#include <os.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "option.h"
#include <crfsuite.h>
#include <crfsuite.hpp>


#define    APPLICATION_S    "CRFSuite"

using namespace CRFSuite;


int main(int argc, char *argv[])
{


	// Teste
	Trainer * trainer = new CRFSuite::Trainer();

	ItemSequence c_seq;

	Item item;
	item.push_back(Attribute("1-1", 1));
	item.push_back(Attribute("1-2", 1));
	item.push_back(Attribute("1-3", 1));
	c_seq.push_back(item);
	Item item2;
	item2.push_back(Attribute("2-1", 1));
	item2.push_back(Attribute("2-2", 1));
	item2.push_back(Attribute("2-3", 1));
	c_seq.push_back(item2);
	Item item3;
	item3.push_back(Attribute("3-1", 1));
	item3.push_back(Attribute("3-2", 1));
	item3.push_back(Attribute("3-3", 1));
	c_seq.push_back(item3);

	Patterns patterns;
	
	Pattern my_pattern1;
	my_pattern1.lines.push_back(0);
	my_pattern1.lines.push_back(1);
	my_pattern1.columns.push_back(0);

	Pattern my_pattern2;
	my_pattern2.lines.push_back(1);
	my_pattern2.columns.push_back(0);

	Pattern my_pattern3;
	my_pattern3.lines.push_back(2);
	my_pattern3.columns.push_back(0);

	Pattern my_pattern4;
	my_pattern4.lines.push_back(-1);
	my_pattern4.columns.push_back(0);

	Pattern my_pattern5;
	my_pattern5.lines.push_back(-2);
	my_pattern5.lines.push_back(-1);
	my_pattern5.columns.push_back(0);

	Pattern my_pattern6;
	my_pattern6.lines.push_back(-2);
	my_pattern6.lines.push_back(-1);
	my_pattern6.lines.push_back(0);
	my_pattern6.lines.push_back(1);
	my_pattern6.lines.push_back(2);
	my_pattern6.columns.push_back(0);


	patterns.push_back(my_pattern1);
	patterns.push_back(my_pattern2);
	patterns.push_back(my_pattern3);
	patterns.push_back(my_pattern4);
	patterns.push_back(my_pattern5);
	patterns.push_back(my_pattern6);



	ItemSequence seq =  CRFSuite::full_make_patterns(patterns, c_seq);

	//trainer->append(c_seq);




	return 0;

}
