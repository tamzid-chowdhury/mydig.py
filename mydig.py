import dns
import dns.message
import dns.query
import dns.name
import sys 
import time
import math

#extract domain name
domain = sys.argv[1]

time_start = time.time()
query_date = time.localtime()

#instantiate a Name object
qname = dns.name.from_text(domain)



#create quary message
root_query = dns.message.make_query(qname,dns.rdatatype.A)



#query the root server
root_response = dns.query.udp(root_query, '192.33.4.12')

#get an ip address for tld
tld_ip_address = root_response.additional[0][0]

#query tld server
tld_response = dns.query.udp(root_query, str(tld_ip_address))

if(not tld_response.additional): #if no ip address make query with NS
    
    domain = str(tld_response.authority[0][0])
    qname = dns.name.from_text(domain)
    root_query = dns.message.make_query(qname,dns.rdatatype.A)
    root_response = dns.query.udp(root_query, '192.33.4.12')
    
    tld_ip_address = root_response.additional[0][0]

    tld_response = dns.query.udp(root_query, str(tld_ip_address))


    if len(tld_response.additional) > 1:
        authorative_ip = tld_response.additional[0][0] 
    else:
        authorative_ip = tld_response.additional[1][0]

else:  
    
    if len(tld_response.additional) > 1:
        authorative_ip = tld_response.additional[1][0] #if > 1 additional[0][0] is AAAA which we cannot resolve
    else:
        authorative_ip = tld_response.additional[0][0]

authorative_response = dns.query.udp(root_query, str(authorative_ip))

#calculate time elapsed for query in msec
time_end = time.time()
query_time = (time_end - time_start) * 1000

#Output 
print("QUESTION SECTION:")
for data in authorative_response.question:
    print(data)
    print("")

print("ANSWER SECTION:")
for data in authorative_response.answer:
    print(data)
    print("")

print("Query time: " + str(math.trunc(query_time)) + " msec")
print("WHEN: " + time.asctime(query_date))
