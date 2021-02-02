import ffmpeg
import json

#A class that orginizes the video-derived data according to the JSON file.
class VideoDataProcessor:
    def __init__(self,path):
        #Initial Values for the class' variable
        
        #A list of 2-value lists which declare the start and the end for the valid parts of the video - [end of the previous freeze, start of the next freeze]
        self.valids = [[0,0]]

        #A variable who stores the longest valid period's length.
        self.maxValid = 0

        #A variable who stores the percentage of the valid parts from the entire video
        self.valid_percentage = 0

        #A flag for validating the pathfile
        self.correct_path = True

        #Validationg the pathfile
        try:
            stream  = ffmpeg.input(path)
        except:
            self.correct_path = False

        if (self.correct_path == True):
            stream  = ffmpeg.filter(stream, 'freezedetect', n=0.003).output('current_freeze.txt') #Extracting the filter's metadata and retrieve it on a given text file.
            counter = 0 #line counter
            fz_durations = 0 #variable for summing the times of the freeze moments.
            for line in open('current_freeze.txt','r').readlines(): #reading the text file for the filter's metadata and creating the full list of valid periods.
                num  = float(line[-1][:-1])
                if counter % 3 == 0: #start freeze
                    self.valids[-1][1] = num
                    self.maxValid = max(self.valids[-1][1]-self.valids[-1][0],self.maxValid)
                elif counter % 2 == 1: #duration of the freeze
                    fz_durations = fz_durations + num
                else: #end of the freeze
                    self.valids.append([0,0])
                    self.valids[-1][0] = num
                    
                counter= counter+1
                
            video_duration = self.valids[-1][0] # = the last "end freeze" of the video
            self.valid_percentage = (video_duration - fz_durations)/video_duration
            self.valids = self.valids[:-1]

    #Create a dictionary based on the video data and according to the JSON file's form
    def create_dict(self):
        out_dict = dict()
        if (self.correct_path == True):
            out_dict["longest_valid_period"] = self.maxValid
            out_dict["valid_video_percentage"] = self.valid_percentage
            out_dict["valid_periods"] = self.valids

        return out_dict

#A class for maintaing the final JSON file for analyzing a series of videos.
class FreezeDetector:
    def __init__(self,paths):
        self.video_data = []
        self.syncflag = True #Flag for declaring if all the pathfiles are valid
        for pt in paths:
            curr_proc = VideoDataProcessor(pt)
            if (curr_proc.correct_path == True):
                self.video_data.append(curr_proc.create_dict())
            else:
                self.syncflag = False
                
    def create_json(self):
        convDict = dict()
        convDict["all_videos_freeze_frame_synced"] = self.syncflag
        convDict["videos"] = self.video_data

        with open("output.json", "w") as outfile: #Converting the final dictionary into a given json file
            json.dump(convDict, outfile)

if __name__ == '__main__':
    paths = ['freeze_frame_input_a.mp4','freeze_frame_input_b.mp4','freeze_frame_input_c.mp4']
    FreezeDetector(paths)
    
        
                    
                    
                    
                    
                
            
