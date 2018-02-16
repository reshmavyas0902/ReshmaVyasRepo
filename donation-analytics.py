#!/usr/bin/env python
"""



"""
import sys
import math
import os
def get_percentile(given_filename = "percentile.txt"):
	try:
		with open(given_filename,"r") as f:
			lines = f.readlines()
			if not lines:
				print >> sys.stderr, "no percentile goven\n"
				sys.exit(1)
			else:
				try:
					temp_int = int(lines[0])
				except TypeError as e:
					print >> sys.stderr, "not a valid integer in file = %s\n" %(given_filename)
					sys.exit(3)
				else:
					if 0 <= temp_int <= 100:
						return temp_int
					else:
						print >> sys.stderr, "percentile should be integer between 0 and 100 in file = %s\n" %(given_filemname)
						sys.exit(2) 
	except IOError as e:
		print >> sys.stderr,"%s\n" %(e)



def get_data(given_filename = "itcont.txt"):
	try:
		with open(given_filename,"r") as f:
			lines= f.readlines()
			if not lines:
				print >> sys.stderr, "given file = %s is empty\n" %(given_filename)
				sys.exit(6)
			else:
				return lines
		
	except FileNotFoundError as e:
		print >> sys.stderr, "file = %s is not found\n" %(given_filename)
		sys.exit(5)
	else:
		pass

def create_dictionary_from_record(given_line = "",minimum_field = 17,given_percential = 100,given_record_id = -1):
	return_dictionary = {}
	percential = given_percential # -1 percentile specifies that it is not determined,to be determined in future 
	record = given_record_id # -1 record specifies that it is not determined,to be determined in future
	other_id = -1 # -1 specifies that it is not determined,to be determined in future
        rep_don = "no"
	if not given_line:
		return {}
	else:
		temp_record = given_line.split("|")
		if len(temp_record) < minimum_field:
			print >> sys.stderr, "incorrect record length in line = %s should be greater then  %d found = %d ignoring this line \n" %(line,minimum_field,len(temp_record))
			
		else:
			               
			temp_date = temp_record[13]
			if len(temp_record[13]) >= 8:
				temp_tuple_keym =	(recipient,zip,year,name,amount,percential,record,other_id) = (temp_record[0],temp_record[10],temp_record[13][4:],temp_record[7],temp_record[14],percential,record,temp_record[15]) 	
			else:
				print >> sys.stderr, "inavalid date and time = %s\n" %(temp_record[7])
				return {}
			if other_id:
				return {}
			else:
				zip = zip[0:5]			
				tuple_key = (zip,name,rep_don)
                return_dictionary[tuple_key] = [[year],[amount],[False],percential,record,recipient]
                return return_dictionary

if __name__=='__main__':
	overall_dict = {}
	grand_total = -1.0
	temp_file = "temp_output.txt"
	if len(sys.argv) >= 3:
		input_file_itcont = sys.argv[1]
		input_file_percentile = sys.argv[2]
		output_file = sys.argv[3]
	else:
		input_file_itconf = "../input/itcont.txt"
		input_file_percentile = "../input/percentile.txt"
		output_file = "../output/repeat_donors.txt"
	try:
		os.remove(temp_file)
		os.remove(output_file)	
	except OSError as e:
		pass
	else:
		pass
	percentile = get_percentile(given_filename = input_file_percentile)
	lines = get_data(given_filename= input_file_itcont)
	for line in lines:
  		temp_dict = create_dictionary_from_record(given_line = line,given_percential = percentile)
		if not temp_dict:
			continue
		else:
			try:

				if temp_dict.keys()[0] not in overall_dict.keys():	
					overall_dict.update(temp_dict)	
				else:   
                                        output_key = temp_dict[temp_dict.keys()[0]]
                                        x=int(output_key[1][0])
				        zip,name,re_donor = temp_dict.keys()[0]
					#zip = zip[0:5]	
					temp_amount = overall_dict[temp_dict.keys()[0]][1][0]
					temp_amount_int = int(temp_amount)
					with open("temp_output.txt","a") as f:
						#line = "%s|%s|%s|%s|%s|%s" %(output_key[-1],zip,name,output_key[0][0],temp_amount_int + int(output_key[1][0]),output_key[2])
						if grand_total <= 0: 
							line = "%s|%s|%s|%s" %(output_key[-1],zip,output_key[0][0],output_key[1][0])
							grand_total = float(output_key[1][0])
						else:
							grand_total += float(output_key[1][0])
							line = "%s|%s|%s|%s" %(output_key[-1],zip,output_key[0][0],str(grand_total))
						f.write(line)
						f.write("\r\n")
					update_key = 	temp_dict.keys()[0]	
					overall_dict[update_key][0].append(temp_dict[update_key][0][0])
					overall_dict[update_key][1].append(temp_dict[update_key][1][0])
					overall_dict[update_key][2].append(temp_dict[update_key][2][0])
					last_amt=int(output_key[1][0])
			except KeyError as e:
				overall_dict.update(temp_dict)	
	# now all records have been read and dictionary is created ,compute percentile and print records
	record_id = 1 
	with open(temp_file,"r") as f:
		lines = f.readlines()
		count = len(lines)
		data_list = [] 
		percentile_calculated = (percentile * count  )  / 100.0
		for line in lines:
	        	data_list.append(line.split("|")[-1])
		data_list.sort()
		percentile_calculated = math.ceil(percentile_calculated)
		percentile_calculated = data_list[int((percentile_calculated -1))]
		with open(output_file,"w") as f2:
			for line in lines:
				if not line:
					continue
				temp_list = line.strip().split("|")
                                temp_str = str(percentile_calculated)
				temp_list.insert(3,temp_str.strip())	
				temp_str = str(record_id)
				temp_list.append(temp_str.strip())
				f2.write("|".join(temp_list))
				f2.write("\r\n")
				record_id += 1
