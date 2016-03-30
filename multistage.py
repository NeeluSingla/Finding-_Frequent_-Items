import sys
import itertools

def hashFuncOne(items,bucket_size):  #add ascii bucket values and return modulo bucket size
	sum = 0
	for item in items:
		sum += ord(item)
	return sum%bucket_size

def hashFuncTwo(items,bucket_size):  #add ascii bucket values and return modulo 20
	sum = 0
	for item in items:
		sum += ord(item) - 3
	return abs(sum)%bucket_size

def createBitmap(bucket_list):
	bitmap = 0;
	for bucket in bucket_list:
		if bucket_list[bucket] >= support:
			bitmap = bitmap | (1<<bucket)
	return bitmap



if __name__ == "__main__":
	support,bucket_size = int(sys.argv[2]),int(sys.argv[3])
	bitmap_one,bitmap_two = 0,0
	frequent_items = []
	candidate_pairs = []
	for pass_step in range(1,8):
		count_candidates,hash_bucket_one,hash_bucket_two = {},{},{}
		#stage 1
		inputdata = open(sys.argv[1])
		for basket in inputdata:
			basket_array = sorted(basket.strip().split(","))

			candidates = [list(x) for x in itertools.combinations(basket_array,pass_step)]
			for candidate in candidates:
				avoid = False
				if candidate_pairs:
					if not candidate in candidate_pairs:
						avoid = True

				if avoid!=True:
					if not tuple(candidate) in count_candidates:
						count_candidates[tuple(candidate)] = 1
					else:
						count_candidates[tuple(candidate)] +=1



			#Hash next step candidates to the table
			hash_candidates = [list(x) for x in itertools.combinations(basket_array,pass_step+1)]
			hash_bucket_one = dict([ (i ,0) for i in range(bucket_size)])
			# print hash_bucket_one
			# sys.exit()

			for hash_candidate in hash_candidates:
				hash_map_key_one = hashFuncOne(hash_candidate,bucket_size)
				if not hash_map_key_one in hash_bucket_one:
					hash_bucket_one[hash_map_key_one] = 1
				else:
					hash_bucket_one[hash_map_key_one] += 1
		if pass_step == 1:
			print ("memory for item counts:",len(count_candidates)*8)
			print ("memory for hash table 1 counts for size "+str(pass_step+1)+" itemsets:",len(hash_bucket_one)*4)
			print  (hash_bucket_one)
		candidate_pairs = []

		#stage 2
		frequent_items = sorted([ list(item) for item in count_candidates if count_candidates[item] >= support])
		#print "memory for item counts:",len(count_candidates)
		print ("frequent itemsets of size "+str(pass_step)+":",frequent_items)

		print ("\nmemory for frequent itemsets of size "+str(pass_step)+" :",len(frequent_items)*(pass_step+1)*4)
		bitmap_one = createBitmap(hash_bucket_one)
		print ("bitmap 1 size:", len(hash_bucket_one))


		inputdata = open(sys.argv[1])
		for basket in inputdata:
			basket_array = sorted(basket.strip().split(","))

			hash_candidates = [list(x) for x in itertools.combinations(basket_array,pass_step+1)]
			hash_bucket_two = dict([ (i ,0) for i in range(bucket_size)])
			for hash_candidate in hash_candidates:

				avoid = False
				if bitmap_one:
					hash_map_key_one = hashFuncOne(hash_candidate,bucket_size)
					if(bitmap_one & (1<<hash_map_key_one) == 0):
						avoid = True

				subsets = [list(x) for x in itertools.combinations(hash_candidate,pass_step)]

				if len(frequent_items)>0:
					for subset in subsets:
						if not subset in frequent_items:
							avoid =True

				if (avoid != True):
					hash_map_key_two = hashFuncTwo(hash_candidate,bucket_size)
					if not hash_map_key_two in hash_bucket_two:
						hash_bucket_two[hash_map_key_two] = 1
					else:
						hash_bucket_two[hash_map_key_two] +=1
		print ("memory for hash table 2 counts for size "+str(pass_step+1)+" itemsets:",len(hash_bucket_one)*4)
		print (hash_bucket_two)

		#stage 3
		bitmap_two = createBitmap(hash_bucket_two)
		print ("\nmemory for frequent itemsets of size "+str(pass_step)+" :",len(frequent_items)*(pass_step+1)*4)
		print ("bitmap 1 size:", len(hash_bucket_one))
		print ("bitmap 2 size:", len(hash_bucket_two))

		inputdata = open(sys.argv[1])
		for basket in inputdata:
			basket_array = sorted(basket.strip().split(","))
			hash_candidates = [list(x) for x in itertools.combinations(basket_array,pass_step+1)]
			for hash_candidate in hash_candidates:
				avoid = False
				if bitmap_one:
					hash_map_key_one = hashFuncOne(hash_candidate,bucket_size)
					if(bitmap_one & (1<<hash_map_key_one) == 0):
						avoid = True

				#if bitmap two
				if bitmap_two:
					hash_map_key_two = hashFuncTwo(hash_candidate,bucket_size)
					if(bitmap_two & (1<<hash_map_key_two) == 0):
						avoid = True

				subsets = [list(x) for x in itertools.combinations(hash_candidate,pass_step)]
				if len(frequent_items)>0:
					for subset in subsets:
						if not subset in frequent_items:
							avoid =True

				if (avoid != True):
					if not hash_candidate in candidate_pairs:
						candidate_pairs.append(hash_candidate)
		print ("memory for candidates of size  "+str(pass_step+1)+" :", len(candidate_pairs)*(pass_step+2)*4,"\n")
		if len(candidate_pairs)<1:
			break
		#print candidate_pairs
			#sys.exit()
