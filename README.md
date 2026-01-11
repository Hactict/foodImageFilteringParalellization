# foodImageFilteringParalellization
In GCP, please use e2 highcpu 4cpu

# Update system
sudo apt update

sudo apt install -y python3-pip python3-venv

# Create virtual environment
python3 -m venv venv

source venv/bin/activate

# Install required libraries
pip install numpy pillow pandas matplotlib

# Install scipy 
pip install scipy

# Install Unzip
sudo apt install unzip -y

#Upload Zip file
Upload download zip file from github

#Unzip file
unzip foodImageFilteringParalellization-main.zip

# 1. Test quick mode first
python run_complete_benchmark_3way.py  -- quick 

# 2. Check outputs are generated
ls food_images/output_multiprocessing/

ls food_images/output_concurrent/

# 3. Verify charts are created
ls performance_charts/

# 4. Run full benchmark
python run_complete_benchmark_3way.py  

# 5. Review performance summary
cat performance_charts/performance_summary.txt


View  performance_charts

sudo apt install zip

zip -r charts_results.zip ~/performance_charts

Kalau gambar

zip -r image_results.zip ~/food_images



1. Download via Google Cloud Console

In your SSH browser window, look at the top right corner and click the Download File button (icon with a down arrow).

In the File path field, type: charts_results.zip

Click Download. The file will appear in your local PC's Downloads folder.
