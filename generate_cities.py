#!/usr/bin/env python3
"""
Script to generate comprehensive city data for all major cities in India
"""

# Major cities data for all states and union territories of India
CITIES_DATA = {
    # Delhi
    "Delhi": {"lat": 28.7041, "lon": 77.1025, "state": "Delhi"},
    "New Delhi": {"lat": 28.6139, "lon": 77.2090, "state": "Delhi"},
    
    # Maharashtra
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "state": "Maharashtra"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "state": "Maharashtra"},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882, "state": "Maharashtra"},
    "Thane": {"lat": 19.2183, "lon": 72.9781, "state": "Maharashtra"},
    "Nashik": {"lat": 19.9975, "lon": 73.7898, "state": "Maharashtra"},
    "Aurangabad": {"lat": 19.8762, "lon": 75.3433, "state": "Maharashtra"},
    "Solapur": {"lat": 17.6599, "lon": 75.9064, "state": "Maharashtra"},
    "Kolhapur": {"lat": 16.7050, "lon": 74.2433, "state": "Maharashtra"},
    "Amravati": {"lat": 20.9374, "lon": 77.7796, "state": "Maharashtra"},
    "Nanded": {"lat": 19.1383, "lon": 77.3210, "state": "Maharashtra"},
    
    # Karnataka
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "state": "Karnataka"},
    "Mysore": {"lat": 12.2958, "lon": 76.6394, "state": "Karnataka"},
    "Hubli": {"lat": 15.3647, "lon": 75.1240, "state": "Karnataka"},
    "Mangalore": {"lat": 12.9141, "lon": 74.8560, "state": "Karnataka"},
    "Belgaum": {"lat": 15.8497, "lon": 74.4977, "state": "Karnataka"},
    "Gulbarga": {"lat": 17.3297, "lon": 76.8343, "state": "Karnataka"},
    "Davanagere": {"lat": 14.4644, "lon": 75.9218, "state": "Karnataka"},
    "Bellary": {"lat": 15.1394, "lon": 76.9214, "state": "Karnataka"},
    "Bijapur": {"lat": 16.8244, "lon": 75.7154, "state": "Karnataka"},
    "Shimoga": {"lat": 13.9299, "lon": 75.5681, "state": "Karnataka"},
    
    # Uttar Pradesh
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "state": "Uttar Pradesh"},
    "Kanpur": {"lat": 26.4499, "lon": 80.3319, "state": "Uttar Pradesh"},
    "Varanasi": {"lat": 25.3176, "lon": 82.9739, "state": "Uttar Pradesh"},
    "Agra": {"lat": 27.1767, "lon": 78.0081, "state": "Uttar Pradesh"},
    "Prayagraj": {"lat": 25.4358, "lon": 81.8463, "state": "Uttar Pradesh"},
    "Ghaziabad": {"lat": 28.6692, "lon": 77.4538, "state": "Uttar Pradesh"},
    "Noida": {"lat": 28.5355, "lon": 77.3910, "state": "Uttar Pradesh"},
    "Meerut": {"lat": 28.9845, "lon": 77.7064, "state": "Uttar Pradesh"},
    "Bareilly": {"lat": 28.3670, "lon": 79.4304, "state": "Uttar Pradesh"},
    "Aligarh": {"lat": 27.8974, "lon": 78.0880, "state": "Uttar Pradesh"},
    "Moradabad": {"lat": 28.8389, "lon": 78.7738, "state": "Uttar Pradesh"},
    "Saharanpur": {"lat": 29.9675, "lon": 77.5536, "state": "Uttar Pradesh"},
    "Gorakhpur": {"lat": 26.7606, "lon": 83.3732, "state": "Uttar Pradesh"},
    "Faizabad": {"lat": 26.7775, "lon": 82.1451, "state": "Uttar Pradesh"},
    "Jhansi": {"lat": 25.4484, "lon": 78.5685, "state": "Uttar Pradesh"},
    
    # Tamil Nadu
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "state": "Tamil Nadu"},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "state": "Tamil Nadu"},
    "Madurai": {"lat": 9.9252, "lon": 78.1198, "state": "Tamil Nadu"},
    "Salem": {"lat": 11.6643, "lon": 78.1460, "state": "Tamil Nadu"},
    "Tiruchirappalli": {"lat": 10.7905, "lon": 78.7047, "state": "Tamil Nadu"},
    "Vellore": {"lat": 12.9165, "lon": 79.1325, "state": "Tamil Nadu"},
    "Erode": {"lat": 11.3410, "lon": 77.7172, "state": "Tamil Nadu"},
    "Tiruppur": {"lat": 11.1085, "lon": 77.3411, "state": "Tamil Nadu"},
    "Thoothukkudi": {"lat": 8.7642, "lon": 78.1348, "state": "Tamil Nadu"},
    "Dindigul": {"lat": 10.3629, "lon": 77.9754, "state": "Tamil Nadu"},
    "Thanjavur": {"lat": 10.7869, "lon": 79.1378, "state": "Tamil Nadu"},
    "Ranipet": {"lat": 12.9279, "lon": 79.3302, "state": "Tamil Nadu"},
    
    # West Bengal
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "state": "West Bengal"},
    "Howrah": {"lat": 22.5958, "lon": 88.2636, "state": "West Bengal"},
    "Durgapur": {"lat": 23.5204, "lon": 87.3119, "state": "West Bengal"},
    "Asansol": {"lat": 23.6889, "lon": 86.9661, "state": "West Bengal"},
    "Siliguri": {"lat": 26.7271, "lon": 88.3953, "state": "West Bengal"},
    "Bardhaman": {"lat": 23.2324, "lon": 87.8555, "state": "West Bengal"},
    "Malda": {"lat": 25.0119, "lon": 88.1324, "state": "West Bengal"},
    "Baharampur": {"lat": 24.1047, "lon": 88.2515, "state": "West Bengal"},
    "Habra": {"lat": 22.8420, "lon": 88.6296, "state": "West Bengal"},
    "Kharagpur": {"lat": 22.3460, "lon": 87.2320, "state": "West Bengal"},
    
    # Telangana
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "state": "Telangana"},
    "Warangal": {"lat": 17.9689, "lon": 79.5941, "state": "Telangana"},
    "Nizamabad": {"lat": 18.6725, "lon": 78.0941, "state": "Telangana"},
    "Karimnagar": {"lat": 18.4386, "lon": 79.1288, "state": "Telangana"},
    "Ramagundam": {"lat": 18.8000, "lon": 79.4500, "state": "Telangana"},
    "Khammam": {"lat": 17.2473, "lon": 80.1514, "state": "Telangana"},
    "Mahbubnagar": {"lat": 16.7362, "lon": 77.9882, "state": "Telangana"},
    "Nalgonda": {"lat": 17.0544, "lon": 79.2670, "state": "Telangana"},
    "Adilabad": {"lat": 19.6633, "lon": 78.5320, "state": "Telangana"},
    "Siddipet": {"lat": 18.1048, "lon": 78.8486, "state": "Telangana"},
    
    # Gujarat
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "state": "Gujarat"},
    "Surat": {"lat": 21.1702, "lon": 72.8311, "state": "Gujarat"},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812, "state": "Gujarat"},
    "Rajkot": {"lat": 22.3039, "lon": 70.8022, "state": "Gujarat"},
    "Bhavnagar": {"lat": 21.7645, "lon": 72.1519, "state": "Gujarat"},
    "Jamnagar": {"lat": 22.4707, "lon": 70.0577, "state": "Gujarat"},
    "Gandhinagar": {"lat": 23.2156, "lon": 72.6369, "state": "Gujarat"},
    "Anand": {"lat": 22.5645, "lon": 72.9289, "state": "Gujarat"},
    "Bharuch": {"lat": 21.7051, "lon": 72.9959, "state": "Gujarat"},
    "Junagadh": {"lat": 21.5222, "lon": 70.4579, "state": "Gujarat"},
    
    # Rajasthan
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "state": "Rajasthan"},
    "Jodhpur": {"lat": 26.2389, "lon": 73.0243, "state": "Rajasthan"},
    "Kota": {"lat": 25.2138, "lon": 75.8648, "state": "Rajasthan"},
    "Bikaner": {"lat": 28.0229, "lon": 73.3119, "state": "Rajasthan"},
    "Ajmer": {"lat": 26.4499, "lon": 74.6399, "state": "Rajasthan"},
    "Udaipur": {"lat": 24.5854, "lon": 73.7125, "state": "Rajasthan"},
    "Bhilwara": {"lat": 25.3463, "lon": 74.6364, "state": "Rajasthan"},
    "Alwar": {"lat": 27.5665, "lon": 76.6108, "state": "Rajasthan"},
    "Sri Ganganagar": {"lat": 29.9038, "lon": 73.8772, "state": "Rajasthan"},
    "Sikar": {"lat": 27.6093, "lon": 75.1397, "state": "Rajasthan"},
    
    # Madhya Pradesh
    "Bhopal": {"lat": 23.2599, "lon": 77.4126, "state": "Madhya Pradesh"},
    "Indore": {"lat": 22.7196, "lon": 75.8577, "state": "Madhya Pradesh"},
    "Jabalpur": {"lat": 23.1815, "lon": 79.9864, "state": "Madhya Pradesh"},
    "Gwalior": {"lat": 26.2183, "lon": 78.1828, "state": "Madhya Pradesh"},
    "Ujjain": {"lat": 23.1765, "lon": 75.7885, "state": "Madhya Pradesh"},
    "Sagar": {"lat": 23.8388, "lon": 78.7378, "state": "Madhya Pradesh"},
    "Dewas": {"lat": 22.9623, "lon": 76.0508, "state": "Madhya Pradesh"},
    "Satna": {"lat": 24.5854, "lon": 80.8292, "state": "Madhya Pradesh"},
    "Ratlam": {"lat": 23.3343, "lon": 75.0376, "state": "Madhya Pradesh"},
    "Rewa": {"lat": 24.5373, "lon": 81.3042, "state": "Madhya Pradesh"},
    
    # Andhra Pradesh
    "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185, "state": "Andhra Pradesh"},
    "Vijayawada": {"lat": 16.5062, "lon": 80.6480, "state": "Andhra Pradesh"},
    "Guntur": {"lat": 16.2991, "lon": 80.4575, "state": "Andhra Pradesh"},
    "Nellore": {"lat": 14.4426, "lon": 79.9865, "state": "Andhra Pradesh"},
    "Kurnool": {"lat": 15.8281, "lon": 78.0373, "state": "Andhra Pradesh"},
    "Rajahmundry": {"lat": 17.0005, "lon": 81.8040, "state": "Andhra Pradesh"},
    "Kakinada": {"lat": 16.9891, "lon": 82.2475, "state": "Andhra Pradesh"},
    "Tirupati": {"lat": 13.6288, "lon": 79.4192, "state": "Andhra Pradesh"},
    "Anantapur": {"lat": 14.6819, "lon": 77.6006, "state": "Andhra Pradesh"},
    "Kadapa": {"lat": 14.4753, "lon": 78.8354, "state": "Andhra Pradesh"},
    
    # Kerala
    "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366, "state": "Kerala"},
    "Kochi": {"lat": 9.9312, "lon": 76.2673, "state": "Kerala"},
    "Kozhikode": {"lat": 11.2588, "lon": 75.7804, "state": "Kerala"},
    "Thrissur": {"lat": 10.5276, "lon": 76.2144, "state": "Kerala"},
    "Kollam": {"lat": 8.8932, "lon": 76.6141, "state": "Kerala"},
    "Alappuzha": {"lat": 9.4981, "lon": 76.3388, "state": "Kerala"},
    "Palakkad": {"lat": 10.7867, "lon": 76.6548, "state": "Kerala"},
    "Kannur": {"lat": 11.8745, "lon": 75.3704, "state": "Kerala"},
    "Kottayam": {"lat": 9.5916, "lon": 76.5222, "state": "Kerala"},
    "Pathanamthitta": {"lat": 9.2647, "lon": 76.7870, "state": "Kerala"},
    
    # Punjab
    "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "state": "Punjab"},
    "Amritsar": {"lat": 31.6340, "lon": 74.8723, "state": "Punjab"},
    "Jalandhar": {"lat": 31.3260, "lon": 75.5762, "state": "Punjab"},
    "Patiala": {"lat": 30.3398, "lon": 76.3869, "state": "Punjab"},
    "Bathinda": {"lat": 30.2110, "lon": 74.9455, "state": "Punjab"},
    "Pathankot": {"lat": 32.2743, "lon": 75.6527, "state": "Punjab"},
    "Hoshiarpur": {"lat": 31.5320, "lon": 75.9170, "state": "Punjab"},
    "Moga": {"lat": 30.8168, "lon": 75.1688, "state": "Punjab"},
    "Firozpur": {"lat": 30.9254, "lon": 74.6133, "state": "Punjab"},
    "Sangrur": {"lat": 30.2453, "lon": 75.8449, "state": "Punjab"},
    
    # Haryana
    "Gurgaon": {"lat": 28.4595, "lon": 77.0266, "state": "Haryana"},
    "Faridabad": {"lat": 28.4089, "lon": 77.3178, "state": "Haryana"},
    "Panipat": {"lat": 29.3909, "lon": 76.9635, "state": "Haryana"},
    "Yamunanagar": {"lat": 30.1290, "lon": 77.2674, "state": "Haryana"},
    "Rohtak": {"lat": 28.8955, "lon": 76.6066, "state": "Haryana"},
    "Hisar": {"lat": 29.1492, "lon": 75.7217, "state": "Haryana"},
    "Karnal": {"lat": 29.6857, "lon": 76.9905, "state": "Haryana"},
    "Sonipat": {"lat": 28.9931, "lon": 77.0151, "state": "Haryana"},
    "Panchkula": {"lat": 30.6942, "lon": 76.8606, "state": "Haryana"},
    "Ambala": {"lat": 30.3752, "lon": 76.7821, "state": "Haryana"},
    
    # Bihar
    "Patna": {"lat": 25.5941, "lon": 85.1376, "state": "Bihar"},
    "Gaya": {"lat": 24.7914, "lon": 85.0002, "state": "Bihar"},
    "Bhagalpur": {"lat": 25.2445, "lon": 86.9718, "state": "Bihar"},
    "Muzaffarpur": {"lat": 26.1209, "lon": 85.3647, "state": "Bihar"},
    "Purnia": {"lat": 25.7771, "lon": 87.4753, "state": "Bihar"},
    "Darbhanga": {"lat": 26.1520, "lon": 85.8970, "state": "Bihar"},
    "Arrah": {"lat": 25.5545, "lon": 84.6624, "state": "Bihar"},
    "Begusarai": {"lat": 25.4180, "lon": 86.1307, "state": "Bihar"},
    "Katihar": {"lat": 25.5335, "lon": 87.5834, "state": "Bihar"},
    "Munger": {"lat": 25.3748, "lon": 86.4735, "state": "Bihar"},
    
    # Odisha
    "Bhubaneswar": {"lat": 20.2961, "lon": 85.8245, "state": "Odisha"},
    "Cuttack": {"lat": 20.4625, "lon": 85.8830, "state": "Odisha"},
    "Rourkela": {"lat": 22.2494, "lon": 84.8828, "state": "Odisha"},
    "Brahmapur": {"lat": 19.3149, "lon": 84.7941, "state": "Odisha"},
    "Sambalpur": {"lat": 21.4704, "lon": 83.9701, "state": "Odisha"},
    "Puri": {"lat": 19.8133, "lon": 85.8315, "state": "Odisha"},
    "Baleshwar": {"lat": 21.4944, "lon": 86.9336, "state": "Odisha"},
    "Baripada": {"lat": 21.9454, "lon": 86.7289, "state": "Odisha"},
    "Bhadrak": {"lat": 21.0590, "lon": 86.4994, "state": "Odisha"},
    "Balangir": {"lat": 20.7076, "lon": 83.4903, "state": "Odisha"},
    
    # Assam
    "Guwahati": {"lat": 26.1445, "lon": 91.7362, "state": "Assam"},
    "Silchar": {"lat": 24.8333, "lon": 92.7789, "state": "Assam"},
    "Dibrugarh": {"lat": 27.4728, "lon": 95.0195, "state": "Assam"},
    "Jorhat": {"lat": 26.7509, "lon": 94.2036, "state": "Assam"},
    "Nagaon": {"lat": 26.3509, "lon": 92.6925, "state": "Assam"},
    "Tinsukia": {"lat": 27.4924, "lon": 95.3574, "state": "Assam"},
    "Tezpur": {"lat": 26.6331, "lon": 92.7925, "state": "Assam"},
    "Sivasagar": {"lat": 26.9849, "lon": 94.6378, "state": "Assam"},
    "Goalpara": {"lat": 26.1769, "lon": 90.6263, "state": "Assam"},
    "Barpeta": {"lat": 26.3224, "lon": 91.0062, "state": "Assam"},
    
    # Jharkhand
    "Ranchi": {"lat": 23.3441, "lon": 85.3096, "state": "Jharkhand"},
    "Jamshedpur": {"lat": 22.8046, "lon": 86.2029, "state": "Jharkhand"},
    "Dhanbad": {"lat": 23.7957, "lon": 86.4304, "state": "Jharkhand"},
    "Bokaro": {"lat": 23.6693, "lon": 86.1511, "state": "Jharkhand"},
    "Deoghar": {"lat": 24.4823, "lon": 86.7000, "state": "Jharkhand"},
    "Phusro": {"lat": 23.7833, "lon": 85.9833, "state": "Jharkhand"},
    "Adityapur": {"lat": 22.7700, "lon": 86.1600, "state": "Jharkhand"},
    "Hazaribagh": {"lat": 23.9924, "lon": 85.3616, "state": "Jharkhand"},
    "Giridih": {"lat": 24.1874, "lon": 86.3095, "state": "Jharkhand"},
    "Ramgarh": {"lat": 23.6307, "lon": 85.5606, "state": "Jharkhand"},
    
    # Chhattisgarh
    "Raipur": {"lat": 21.2514, "lon": 81.6296, "state": "Chhattisgarh"},
    "Bhilai": {"lat": 21.2092, "lon": 81.4285, "state": "Chhattisgarh"},
    "Korba": {"lat": 22.3458, "lon": 82.6963, "state": "Chhattisgarh"},
    "Bilaspur": {"lat": 22.0796, "lon": 82.1391, "state": "Chhattisgarh"},
    "Durg": {"lat": 21.1904, "lon": 81.2849, "state": "Chhattisgarh"},
    "Rajnandgaon": {"lat": 21.0963, "lon": 81.0288, "state": "Chhattisgarh"},
    "Jagdalpur": {"lat": 19.0760, "lon": 82.0354, "state": "Chhattisgarh"},
    "Ambikapur": {"lat": 23.1200, "lon": 83.1950, "state": "Chhattisgarh"},
    "Chirmiri": {"lat": 23.2000, "lon": 82.3500, "state": "Chhattisgarh"},
    "Bhatapara": {"lat": 21.7333, "lon": 81.9333, "state": "Chhattisgarh"},
    
    # Uttarakhand
    "Dehradun": {"lat": 30.3165, "lon": 78.0322, "state": "Uttarakhand"},
    "Haridwar": {"lat": 29.9457, "lon": 78.1642, "state": "Uttarakhand"},
    "Roorkee": {"lat": 29.8543, "lon": 77.8880, "state": "Uttarakhand"},
    "Haldwani": {"lat": 29.2208, "lon": 79.5286, "state": "Uttarakhand"},
    "Rudrapur": {"lat": 28.9800, "lon": 79.4000, "state": "Uttarakhand"},
    "Kashipur": {"lat": 29.2167, "lon": 78.9500, "state": "Uttarakhand"},
    "Rishikesh": {"lat": 30.0869, "lon": 78.2676, "state": "Uttarakhand"},
    "Almora": {"lat": 29.5973, "lon": 79.6570, "state": "Uttarakhand"},
    "Pithoragarh": {"lat": 29.5820, "lon": 80.2189, "state": "Uttarakhand"},
    "Nainital": {"lat": 29.3919, "lon": 79.4542, "state": "Uttarakhand"},
    
    # Himachal Pradesh
    "Shimla": {"lat": 31.1048, "lon": 77.1734, "state": "Himachal Pradesh"},
    "Solan": {"lat": 30.9049, "lon": 77.0965, "state": "Himachal Pradesh"},
    "Mandi": {"lat": 31.7084, "lon": 76.9320, "state": "Himachal Pradesh"},
    "Kullu": {"lat": 31.9578, "lon": 77.1095, "state": "Himachal Pradesh"},
    "Dharamshala": {"lat": 32.2190, "lon": 76.3234, "state": "Himachal Pradesh"},
    "Bilaspur": {"lat": 31.3333, "lon": 76.7500, "state": "Himachal Pradesh"},
    "Chamba": {"lat": 32.5550, "lon": 76.1260, "state": "Himachal Pradesh"},
    "Una": {"lat": 31.4643, "lon": 76.2691, "state": "Himachal Pradesh"},
    "Hamirpur": {"lat": 31.6861, "lon": 76.5206, "state": "Himachal Pradesh"},
    "Kangra": {"lat": 32.1047, "lon": 76.2673, "state": "Himachal Pradesh"},
    
    # Jammu and Kashmir
    "Srinagar": {"lat": 34.0837, "lon": 74.7973, "state": "Jammu and Kashmir"},
    "Jammu": {"lat": 32.7266, "lon": 74.8570, "state": "Jammu and Kashmir"},
    "Anantnag": {"lat": 33.7311, "lon": 75.1486, "state": "Jammu and Kashmir"},
    "Baramulla": {"lat": 34.2090, "lon": 74.3425, "state": "Jammu and Kashmir"},
    "Udhampur": {"lat": 32.9242, "lon": 75.1416, "state": "Jammu and Kashmir"},
    "Kathua": {"lat": 32.3700, "lon": 75.5200, "state": "Jammu and Kashmir"},
    "Rajouri": {"lat": 33.3800, "lon": 74.3000, "state": "Jammu and Kashmir"},
    "Poonch": {"lat": 33.7700, "lon": 74.1000, "state": "Jammu and Kashmir"},
    "Doda": {"lat": 33.1500, "lon": 75.5500, "state": "Jammu and Kashmir"},
    "Kishtwar": {"lat": 33.3200, "lon": 75.7700, "state": "Jammu and Kashmir"},
    
    # Goa
    "Panaji": {"lat": 15.4909, "lon": 73.8278, "state": "Goa"},
    "Margao": {"lat": 15.2993, "lon": 73.9862, "state": "Goa"},
    "Vasco da Gama": {"lat": 15.3860, "lon": 73.8160, "state": "Goa"},
    "Mapusa": {"lat": 15.5910, "lon": 73.8080, "state": "Goa"},
    "Ponda": {"lat": 15.4030, "lon": 74.0150, "state": "Goa"},
    
    # Tripura
    "Agartala": {"lat": 23.8315, "lon": 91.2868, "state": "Tripura"},
    "Udaipur": {"lat": 23.5250, "lon": 91.4850, "state": "Tripura"},
    "Dharmanagar": {"lat": 24.3667, "lon": 92.1667, "state": "Tripura"},
    "Kailasahar": {"lat": 24.3333, "lon": 92.0000, "state": "Tripura"},
    "Belonia": {"lat": 23.2500, "lon": 91.4500, "state": "Tripura"},
    
    # Manipur
    "Imphal": {"lat": 24.8170, "lon": 93.9368, "state": "Manipur"},
    "Thoubal": {"lat": 24.6333, "lon": 93.9833, "state": "Manipur"},
    "Bishnupur": {"lat": 24.6333, "lon": 93.7667, "state": "Manipur"},
    "Churachandpur": {"lat": 24.3333, "lon": 93.6833, "state": "Manipur"},
    "Ukhrul": {"lat": 25.1167, "lon": 94.3667, "state": "Manipur"},
    
    # Meghalaya
    "Shillong": {"lat": 25.5788, "lon": 91.8933, "state": "Meghalaya"},
    "Tura": {"lat": 25.5167, "lon": 90.2167, "state": "Meghalaya"},
    "Jowai": {"lat": 25.4500, "lon": 92.2000, "state": "Meghalaya"},
    "Nongstoin": {"lat": 25.5167, "lon": 91.2667, "state": "Meghalaya"},
    "Williamnagar": {"lat": 25.5000, "lon": 90.6167, "state": "Meghalaya"},
    
    # Mizoram
    "Aizawl": {"lat": 23.7307, "lon": 92.7173, "state": "Mizoram"},
    "Lunglei": {"lat": 22.8833, "lon": 92.7333, "state": "Mizoram"},
    "Saiha": {"lat": 22.4833, "lon": 92.9833, "state": "Mizoram"},
    "Champhai": {"lat": 23.4667, "lon": 93.3333, "state": "Mizoram"},
    "Serchhip": {"lat": 23.3167, "lon": 92.8500, "state": "Mizoram"},
    
    # Nagaland
    "Kohima": {"lat": 25.6751, "lon": 94.1086, "state": "Nagaland"},
    "Dimapur": {"lat": 25.9000, "lon": 93.7333, "state": "Nagaland"},
    "Mokokchung": {"lat": 26.3333, "lon": 94.5167, "state": "Nagaland"},
    "Tuensang": {"lat": 26.2833, "lon": 94.8333, "state": "Nagaland"},
    "Wokha": {"lat": 26.1000, "lon": 94.2667, "state": "Nagaland"},
    
    # Arunachal Pradesh
    "Itanagar": {"lat": 27.0844, "lon": 93.6053, "state": "Arunachal Pradesh"},
    "Naharlagun": {"lat": 27.1000, "lon": 93.7000, "state": "Arunachal Pradesh"},
    "Pasighat": {"lat": 28.0667, "lon": 95.3333, "state": "Arunachal Pradesh"},
    "Tezu": {"lat": 27.9167, "lon": 96.1667, "state": "Arunachal Pradesh"},
    "Ziro": {"lat": 27.6333, "lon": 93.8333, "state": "Arunachal Pradesh"},
    
    # Sikkim
    "Gangtok": {"lat": 27.3389, "lon": 88.6065, "state": "Sikkim"},
    "Namchi": {"lat": 27.1667, "lon": 88.3500, "state": "Sikkim"},
    "Gyalshing": {"lat": 27.2833, "lon": 88.2667, "state": "Sikkim"},
    "Mangan": {"lat": 27.5167, "lon": 88.5333, "state": "Sikkim"},
    "Ravangla": {"lat": 27.3167, "lon": 88.3500, "state": "Sikkim"},
    
    # Union Territories
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "state": "Chandigarh"},
    "Puducherry": {"lat": 11.9416, "lon": 79.8083, "state": "Puducherry"},
    "Port Blair": {"lat": 11.6234, "lon": 92.7265, "state": "Andaman and Nicobar Islands"},
    "Kavaratti": {"lat": 10.5593, "lon": 72.6358, "state": "Lakshadweep"},
    "Silvassa": {"lat": 20.2700, "lon": 72.9500, "state": "Dadra and Nagar Haveli"},
    "Daman": {"lat": 20.3974, "lon": 72.8328, "state": "Daman and Diu"},
    "Leh": {"lat": 34.1526, "lon": 77.5771, "state": "Ladakh"},
    "Kargil": {"lat": 34.5577, "lon": 76.1262, "state": "Ladakh"}
}

def generate_config_file():
    """Generate the updated config.py file with expanded city data"""
    
    config_content = '''# Configuration file for AirScan Lite

# City data with predefined coordinates to avoid API calls
CITY_DATA = {
'''
    
    # Add all cities
    for city, data in CITIES_DATA.items():
        config_content += f'    "{city}": {{"lat": {data["lat"]}, "lon": {data["lon"]}, "state": "{data["state"]}"}},\n'
    
    config_content += '''}

# AQI Categories and their thresholds (PM2.5 values in µg/m³)
AQI_CATEGORIES = {
    "Good": {"min": 0, "max": 30, "color": "green", 
             "message": "Air quality is good. Enjoy outdoor activities!"},
    "Satisfactory": {"min": 31, "max": 60, "color": "lightgreen",
                    "message": "Air quality is satisfactory. Sensitive people may experience minor breathing discomfort."},
    "Moderate": {"min": 61, "max": 90, "color": "yellow",
                "message": "Air quality is moderate. People with heart or lung disease should reduce outdoor activities."},
    "Poor": {"min": 91, "max": 120, "color": "orange",
             "message": "Air quality is poor. Everyone should reduce outdoor activities."},
    "Very Poor": {"min": 121, "max": 250, "color": "red",
                 "message": "Air quality is very poor. Avoid outdoor activities. Use masks if going out."},
    "Severe": {"min": 251, "max": 500, "color": "darkred",
              "message": "Air quality is severe. Stay indoors. Avoid all outdoor activities."}
}

# Weather simulation ranges
WEATHER_RANGES = {
    "temperature": {"min": 15, "max": 35, "unit": "°C"},
    "humidity": {"min": 30, "max": 90, "unit": "%"},
    "wind_speed": {"min": 0, "max": 20, "unit": "km/h"},
    "aod": {"min": 0.1, "max": 1.5, "unit": ""}
}

# ML Model parameters
ML_MODEL = {
    "aod_weight": 50,
    "temperature_weight": 2,
    "variation_range": 0.1,  # ±10% random variation
    "pm25_min": 0,
    "pm25_max": 500
}

# Map configuration
MAP_CONFIG = {
    "zoom_start": 10,
    "width": 800,
    "height": 400
}

# App configuration
APP_CONFIG = {
    "page_title": "AirScan Lite",
    "page_icon": "🌤️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
'''
    
    # Write to config.py
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ Successfully updated config.py with {len(CITIES_DATA)} cities from all states and union territories of India!")
    print(f"📊 Total cities added: {len(CITIES_DATA)}")
    
    # Print summary by state
    states = {}
    for city, data in CITIES_DATA.items():
        state = data["state"]
        if state not in states:
            states[state] = []
        states[state].append(city)
    
    print("\n📋 Cities by State/UT:")
    for state, cities in sorted(states.items()):
        print(f"  {state}: {len(cities)} cities")

if __name__ == "__main__":
    generate_config_file() 