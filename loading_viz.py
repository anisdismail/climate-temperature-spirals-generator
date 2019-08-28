"""This method will create the visualization. It accepts as input
the cleaned dataframe and returns the name of the file where the animation
was created. """

def load_viz(df):
    try:
		#import the method to use to create the animation
        from matplotlib.animation import FuncAnimation 
        from matplotlib.animation import FFMpegWriter

        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        #set the dimensions of the visualization
        fig = plt.figure(figsize=(8,8))

        #set the projection to polar (not cartesian) system
        ax1 = plt.subplot(111, projection='polar')

        #plot the temperature rings at 0,1.5 and 2 
        full_circle_thetas=np.linspace(0,2*np.pi,1000)
        blue_one_radii=[0.0+1.0]*1000
        red_one_radii=[1.5+1.0]*1000
        red_two_radii=[2.0+1.0]*1000
        ax1.plot(full_circle_thetas, blue_one_radii, c='blue')
        ax1.plot(full_circle_thetas, red_one_radii, c='red')
        ax1.plot(full_circle_thetas, red_two_radii, c='red')

        #remove the ticks for both axes
        ax1.set_xticklabels([])
        ax1.set_yticklabels([])

        #set the limit for r axis
        ax1.set_ylim(0,3.25)

        #set the color for the foreground and background
        fig.set_facecolor("#323331")
        ax1.set_facecolor("#000100")

        #add the plot title
        ax1.set_title("Global Temperature Change (1850-{})".format(df["year"].max()),color="white",fontsize=20)
        ax1.set_xticks([])
        ax1.set_yticks([])

        #add the temperatures for the temperature rings
        #ax1.text(np.pi/2, 0.90, "0.0 C", color="blue", ha='center',fontsize= 15)
        ax1.text(np.pi/2, 2.40, "1.5 C", color="red", ha='center', fontsize= 15,bbox=dict(facecolor='#000100', edgecolor='#000100'))
        ax1.text(np.pi/2, 2.90, "2.0 C", color="red", ha='center', fontsize= 15,bbox=dict(facecolor='#000100', edgecolor='#000100'))

        #add the months outer rings
        months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        months_angles= np.linspace((np.pi/2)+(2*np.pi),np.pi/2,13)
        for i,month in enumerate(months):
          ax1.text(months_angles[i],3.4,month,color="white",fontsize=15,ha="center")

        #add the source
        fig.text(0.78,0.01,"HadCRUT 4.6",color="white",fontsize=15)
        fig.text(0.05,0.03,"Anis Ismail",color="white",fontsize=15)
        fig.text(0.05,0.01,"Based on Ed Hawkins's 2017 Visualization",color="white",fontsize=10)

        #prepare the update in each frame function to be used by Funcanimation method
        def update(i):
            # Specify how we want the plot to change in each frame
            # Remove the previous year text at the center of the plot
            for txt in ax1.texts:
              if(txt.get_position()==(0,0)):
                txt.set_visible(False)
                # We need to unravel the for loop we had earlier.
            year = years[i]
            r = df[df['year'] == year]['value'] + 1
            theta = np.linspace(0, 2*np.pi, 12)
            ax1.plot(theta, r, c=plt.cm.viridis(i*2))
            ax1.text(0,0,year,fontsize=20,color="white",ha="center")
            return ax1

        #call the function that will create the animation
        years=df["year"].unique()
        anim = FuncAnimation(fig, update, frames=len(years), interval=10)

        #save the animation
        anim.save('climate_spiral.mp4',writer=FFMpegWriter(),savefig_kwargs={'facecolor': '#323331'})
    except Exception as e:
        #in case of any exception, inform the user
        return "climate_spiral.mp4 was not created successfully,\n \
        Reason:{}".format(e)
    else:
        #else inform the user that the procedure was successful
        return "climate_spiral.mp4 was created successfully"