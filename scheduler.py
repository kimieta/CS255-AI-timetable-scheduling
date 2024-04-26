import comedian
import demographic
import ReaderWriter
import timetable
import random
import math


class Scheduler:

    def __init__(self, comedian_List, demographic_List):
        self.comedian_List = comedian_List
        self.demographic_List = demographic_List

    # Using the comedian_List and demographic_List, create a timetable of 5 slots for each of the 5 work days of the week.
    # The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
    #	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
    # This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj.
    # Note here that the comedian and demographic are represented by objects, not strings.
    # The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
    # The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3.
    # Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists,
    #	your solution will be marked incorrectly.
    # The final, 5th argument, is the show type. For task 1, all shows should be "main". For task 2 and 3, you should assign either "main" or "test" as the show type.
    # In tasks 2 and 3, all shows will either be a 'main' show or a 'test' show

    # demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
    # d.reference  - the reference code of the demographic
    # d.topics - a list of strings, describing the topics that the demographic like to see in their comedy shows e.g. ["Politics", "Family"]

    # comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
    # c.name - the name of the Comedian
    # c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

    # For Task 1:
    # Keep in mind that a comedian can only have their show marketed to a demographic
    # if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
    # Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
    # There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
    # In some problems, demographics will have 2 topics and in others, 3.
    # A comedian will have between 3-8 different themes.

    # For Task 2 and 3:
    # A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
    # that the demographic likes to see in their comedy shows.
    # Comedians can only manage a 4 hours of stage time, where main shows 2 hours and test shows are 1 hour.
    # A Comedian can not be on stage for more than 2 hours a day.

    # You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
    # Furthermore, you should not import anything else beyond what has been imported above.
    # To reiterate, the five calls are timetableObj.addSession, d.name, d.genres, c.name, c.talents
    """ -----------------
    TASK 1 Algorithm:
    Step 1. Create an array of comedians that can perform the show for each demographic in a 2D array where each index 
            corresponds to the index of the demographics 
    Step 2. Schedule all demographics that only one person can do as those people MUST perform those demographics
            using my schedulingSINGLES() 
    Step 3. Schedule the rest of the demographics by the first valid comedian in the list
    ---------------------
    Checking to see if the comedian is valid:
    This is done with the method I created called validComedian() for scheduling both tasks 1 and 2
    ---------------------
    Checking to see if the day is valid:
    This is done with the method I created called validDay() for returning a validDay or False
    When the parameter for task is 1, then it does the following
    Step 1. making sure the day has available slots
    Step 2. making sure the comedian is valid
    Step 3. if either is false, then it will move the day indicator onto the next day until
    - and return the day index if step 1 and 2 are valid
    Step 4. if no days are valid, then it will return False as that comedian cannot perform any more shows
            so the algorithm moves onto the next comedian 
    ---------------------
    Abbreviations for the variables used:
    aofc - array of comedians which can perform that single demographic according to the index of the array
            e.g. aofc[i] = [alice, bob, cat] can do demographic[i] = XYZ123 
            makeAOFC() makes aofc
    ca - 2D of all cia's
            e.g. cia[1] = [kim, counter, [days they have been scheduled],[ hours for those days]]
            comedianSchedulingArray() makes ca
    cia - array of a single comedians information, hours they've done, days scheduled, hours scheduled on those days
    """
    # This method should return a timetable object with a schedule that is legal according to all constraints of task 1.
    def createSchedule(self):
        dayindicator = 0
        tableindex = [0, 0, 0, 0, 0]
        # Do not change this line
        timetableObj = timetable.Timetable(1)

        # Here is where you schedule your timetable
        AOFC = self.makeAOFC("Main")
        ca = self.comedianSchedulingArray(1)
        # SCHEDULING IN shows that require a certain single comedian and updates their counter
        singles = self.schedulingSINGLES(timetableObj, AOFC, ca, tableindex, dayindicator, 1, 0, 5)
        # adding the rest
        for i in range(len(self.demographic_List)):
            for j in range(len(AOFC[i])):
                if i in singles:
                    break
                cia = [x for x in ca if AOFC[i][j] in x][0]
                index = ca.index(cia)
                if self.validDay(tableindex, dayindicator, 5, cia, 1, 1, 0) is not False:
                    dayindicator = self.validDay(tableindex, dayindicator, 5, cia, 1, 1, 0)
                    self.addToTable(timetableObj, tableindex, dayindicator, index, i, "main")
                    self.comedianavaliabilityUpdate(ca, AOFC, dayindicator, -20, 1, i, j)
                    break
        # Do not change this line
        return timetableObj

    # Now, we have introduced test shows. Each day now has ten sessions, and we want to market one main show and one test show
    # to each demographic.
    # All slots must be either a main or a test show, and each show requires a comedian and a demographic.
    # A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
    # We are now concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
    # Main shows are 2 hours, test shows are 1 hour.
    # A comedian can not be on stage for more than 2 hours a day.

    """ -----------------
    TASK 2 Algorithm:
    Step 1. Create an array of comedians that can perform the show for each demographic in a 2D array where each index 
            corresponds to the index of the demographics for both the main and test show
    Step 2. Schedule all demographics that only one person can do as those people MUST perform those demographics
            using my schedulingSINGLES() for the main show - test show should'nt really have any singles
    Step 3. Schedule all the rest of the main shows
    Step 4. Schedule all the test shows
    You should schedule the main shows first as they take up 2h of the comedians time
    when you think about packing/scheduling algorithms, the ones with the biggest times should be going in first
    As the 1h shows after can fit into any of the slots left 
    ---------------------
    Check to see if the comedian is valid with the method I created called validComedian() 
    Check to see if the day is valid with the method I created called validDay()
    """
    def createTestShowSchedule(self):
        dayindicator = 0
        tableindex = [0, 0, 0, 0, 0]
        # Do not change this line
        timetableObj = timetable.Timetable(2)

        # Here is where you schedule your timetable
        aofcMain = self.makeAOFC("Main")
        aofcTest = self.makeAOFC("Test")
        ca = self.comedianSchedulingArray(2)

        # SCHEDULING MAIN SHOWS
        singles = self.schedulingSINGLES(timetableObj, aofcMain, ca, tableindex, dayindicator, 2, 2, 10)
        for i in range(len(self.demographic_List)):
            for j in range(len(aofcMain[i])):
                if i in singles:
                    break
                cia = [x for x in ca if aofcMain[i][j] in x][0] # comedian info array
                index = ca.index(cia)
                if self.validDay(tableindex, dayindicator, 10, cia, 2, 2, 0) is not False:
                    dayindicator = self.validDay(tableindex, dayindicator, 10, cia, 2, 2, 0)
                    self.addToTable(timetableObj, tableindex, dayindicator, index, i, "main")
                    self.comedianavaliabilityUpdate(ca, aofcMain, dayindicator, 2, 2, i, j)
                    break

        # SCHEDULING TRIAL SHOWS
        for i in range(len(self.demographic_List)):
            for j in range(len(aofcTest)):
                cia = [x for x in ca if aofcTest[i][j] in x][0]
                index = ca.index(cia)
                if self.validDay(tableindex, dayindicator, 10, cia, 2, 1, 0) is not False:
                    dayindicator = self.validDay(tableindex, dayindicator, 10, cia, 2, 1, 0)
                    self.addToTable(timetableObj, tableindex, dayindicator, index, i, "test")
                    self.comedianavaliabilityUpdate(ca, aofcTest, dayindicator, 1, 2, i, j)
                    break
                elif self.validDay(tableindex, dayindicator, 10, cia, 2, 1, 0) is False:
                    dayindicator = 0

        return timetableObj

    # It costs £500 to hire a comedian for a single main show.
    # If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
    # If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

    # It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (£200, £150 and £100)
    # If a test shows occur on the same day as anything else a comedian is in, then its cost is halved.

    # Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
    # You are not expected to always find the optimal solution, but you should be as close as possible.
    # You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
    """ -----------------
    concept from: breadth first search
    to get the comedians that can do the maximum number of main or test shows
    concept from: CSP's
    to add main shows and test shows to the timetable and minimise costs
    ---------------------
    Step 1. Get all comedians which can do 2 Main shows to do 2 Main shows and schedule Main shows first
        1.1. collect all comedians that can do 2 main shows
        1.1. schedule adjacent days (mon-tues, wed-thu) 
        1.2. NOT counting (fri-mon) as adjacent
        1.3. any comedian performing 1 single show will perform on the day with the most available slots (probs fri)
    Step 2. Get all comedians which can do 4 Test shows to do 4 Test shows, and then decreasing (i.e. 3, 2, 1)
        2.1. schedule 2 test shows a day where possible 
        2.2. schedule that same comedian to do another 2 test shows on a different day of the week but same day
        2.3. any shows that cannot be scheduled in pairs, schedule to the day with most slots available 
    3. It's no cheaper to schedule a comedian to do a mix of main and test shows, as you cannot have one perform a main and test show on the same day
    ---------------------
    1. minimisingLoops() is used to assign shows to the comedian with the highest counter value 
    (already doing shows) still according to the specification
    2. addOne() adds one comedian to the timetable and updates it according to the parameters
    _____________________
    """
    def createMinCostSchedule(self):
        dayindicator = 0
        tableindex = [0, 0, 0, 0, 0]

        # Do not change this line
        timetableObj = timetable.Timetable(3)

        # Here is where you schedule your timetable
        aofcMain = self.makeAOFC("Main")
        aofcTest = self.makeAOFC("Test")
        ca = self.comedianSchedulingArray(2)

        # MAIN SHOWS
        # Getting as many comedians as possible to do 2 Main shows
        singles = self.schedulingSINGLES(timetableObj, aofcMain, ca, tableindex, dayindicator, 3, -2, 10)
        for i in range(len(self.demographic_List)):
            stage = self.minimisingLoops(ca, singles, aofcMain, -2, 1, -2, i)
            if stage == 2:
                stage = self.minimisingLoops(ca, singles, aofcMain, -2, 2, 0, i)

        # Scheduling main shows, first the ones doing 2 Main shows (to get adj days) ~ (NOTE: counter = -4)
        for i in range(len(ca)):
            if ca[i][1] == -4:
                dayindicator = self.addOne(timetableObj, tableindex, ca, aofcMain, dayindicator, 0, 3.7, 2, 2, i, "main")

        for i in range(len(ca)):
            if ca[i][1] == -2:
                dayindicator = self.addOne(timetableObj, tableindex, ca, aofcMain, dayindicator, 0, 3.62, 1, 2, i, "main")

        # TEST SHOWS
        # Getting as many comedians as possible to do 4 Test shows, then 3, then 2, prioritise bigger numbers
        for i in range(len(self.demographic_List)):
            stage = self.minimisingLoops(ca, singles, aofcTest, 1, 3, 3, i)
            if stage == 4:
                stage = self.minimisingLoops(ca, singles, aofcTest, 1, stage, 2, i)
            if stage == 5:
                stage = self.minimisingLoops(ca, singles, aofcTest, 1, stage, 1, i)
            if stage == 6:
                stage = self.minimisingLoops(ca, singles, aofcTest, 1, stage, 0, i)

        # Scheduling test shows, first the ones doing 4 test shows (to get 2 same day) ~ (NOTE: counter = 4)
        for i in range(len(ca)):
            dayindicator = min(tableindex) # always try schedule on the day with least things
            if ca[i][1] == 4 and self.validDay(tableindex, dayindicator, 10, ca, 3.5, 2, 0) is not False:
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 0, 3.5, 2, 2, i, "test")
            elif ca[i][1] == 4:
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 0, 3.520, 1, 1, i, "test")
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 1, 3.520, 1, 1, i, "test")
            if ca[i][1] == 4 and self.validDay(tableindex, dayindicator + 1, 10, ca[i], 3.52, 2, 0) is not False:
                dayindicator = self.validDay(tableindex, dayindicator + 1, 10, ca[i], 3.52, 2, 0)
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 2, 3.52, 2, 2, i, "test")
            elif ca[i][1] == 4:
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 2, 3.520, 1, 1, i, "test")
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 3, 3.520, 1, 1, i, "test")

        for i in range(len(ca)):
            if (ca[i][1] == 3 or ca[i][1] == 2) and self.validDay(tableindex, dayindicator + 1, 10, ca[i], 3.52, 2, 0) is not False:
                dayindicator = self.validDay(tableindex, dayindicator + 1, 10, ca[i], 3.52, 2, 0)
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 0, 3.52, 2, 2, i, "test")
            elif ca[i][1] == 3 or ca[i][1] == 2:
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 0, 3.520, 1, 1, i, "test")
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 1, 3.520, 1, 1, i, "test")
            if ca[i][1] == 3:
                dayindicator = self.validDay(tableindex, dayindicator, 10, ca[i], 3.520, 1, 0)
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 2, 3.520, 1, 1, i, "test")

        for i in range(len(ca)):
            if ca[i][1] == 1:
                dayindicator = self.validDay(tableindex, dayindicator, 10, ca[i], 3.520, 1, 0)
                self.addOne(timetableObj, tableindex, ca, aofcTest, dayindicator, 0, 3.520, 1, 1, i, "test")

        # Do not change this line
        return timetableObj

    """
    below are the methods I made and used 
    """

    def addToTable(self, timetableObj, timeindexes, dayindicator, index1, index2, type):
        slot = timeindexes[dayindicator] + 1
        timeindexes[dayindicator] = slot
        # each value at the index of the day is a slot
        timetableObj.addSession(self.daytranslator(dayindicator), slot, self.comedian_List[index1], self.demographic_List[index2], type)
        return None

    def schedulingSINGLES(self, timetableObj, AOFC, CA, timeindexes, dayindicator, task, hours, maxslots):
        singles = []
        if task == 3:
            for i in range(len(AOFC)):
                if len(AOFC[i]) == 1:
                    self.comedianavaliabilityUpdate(CA, AOFC, -20, hours, task, i, 0)
                    singles.append(i)
        else:
            for i in range(len(AOFC)):
                if len(AOFC[i]) == 1:
                    comedianInfoArray = [x for x in CA if AOFC[i][0] in x][0]
                    index = CA.index(comedianInfoArray)
                    dayindicator = self.validDay(timeindexes, dayindicator, maxslots, comedianInfoArray, task, hours,0)
                    self.addToTable(timetableObj, timeindexes, dayindicator, index, i, "main")
                    self.comedianavaliabilityUpdate(CA, AOFC, dayindicator, hours, task, i, 0)
                    singles.append(i)
        return singles

    """
    Method to check if the comedian can be scheduled to this day, returns th day index if possible else returns false
    -------------------------------------------------------------------
    Step 1. making sure the day has available slots
    Step 2. making sure the comedian is valid
    Step 3. if either is false, then it will move the day indicator onto the next day until
            and returns the day index if step 1 and 2 are valid
    Step 4. if no days are valid, then it will return False as that comedian cannot perform any more shows
            so the algorithm moves onto the next comedian 
    For task 3.
        - finds adjacent days have enough slots - MAIN SHOWS
        - finds days with 2 slots - TEST SHOWS
        - finds days with 2 slots that isnt the same as the day already scheduled - TEST SHOWS
        - gets day with the most available slots
        - there are alot of different conditions task 3 needs so there are different versions 
    """
    def validDay(self, timeindexes, day, slots, CAArray, task, hours, counter):
        # [monday, tuesday, wednesday, thursday, friday]
        if day > 4:
            day = 0
        # for task 3 I only want to check if the consecutive days are valid or not, one check
        if task == 3.7 and timeindexes[day] < slots and day != 4:
            return day
        elif task == 3.62:
            return timeindexes.index(min(timeindexes))

        if task == 3.5 and timeindexes[day] + hours <= 10:
            return day
        elif task == 3.52 and CAArray[3][0] != day and timeindexes[day] + hours <= 10:
            return day
        elif task == 3.520 and (day not in CAArray[3]) and timeindexes[day] + hours <= 10:
            return day

        if timeindexes[day] < slots and self.validComedian(CAArray, task, hours, day):
            if task == 1:
                return day
            if task == 2 and self.validDay2(CAArray, day, hours):
                return day

        if counter == 5:  # no days available for that comedian
            return False
        day += 1
        counter += 1
        return self.validDay(timeindexes, day, slots, CAArray, task, hours, counter)

    def validDay2(self, CA, day, hours):
        if day not in CA[2]:
            return True
        elif hours == 1:
            otherIndex = CA[2].index(day)
            if CA[3][otherIndex] + hours <= 2:
                return True

        return False

    """
    Method checking if the comedian can perform by returning either true(valid) or false(not-valid)
    ------------------------------------------------------------------------------------
    When the parameter for task is 1:
    Step 1. Making sure the comedian will not be performing more than two shows a week 
    Step 2. Making sure the comedian does not perform more than once a day
    ------------------------------------------------------------------------------------
     When the parameter for task is 2:
     Step 1. Making sure the comedian will not be performing more than 4 hours a week 
     Step 2. Making sure the comedian does not perform more than 2 hours a day 
    """
    def validComedian(self, CAArray, task, showHours, day):
        if task == 1:
            if (CAArray[1] < 2) and ((CAArray[2] == -20) or (CAArray[2] != day)):
                return True
        if task == 2 or task == 3:
            if (CAArray[1] + showHours) > 4:
                return False
            for j in range(4):
                if CAArray[2][j] == -20 and (CAArray[3][j] + showHours) <= 2:
                    return True
        return False

    def minimisingLoops(self, CA, singles, AOFC, hours, stage, indicatingValue, i):
        for j in range(len(AOFC[i])):
            if stage == 1 and (i in singles):
                return stage
            comedianInfoArray = [x for x in CA if AOFC[i][j] in x][0]
            # we will try get as many comedians as possible to do 4 hours of main shows
            if comedianInfoArray[1] == indicatingValue:
                self.comedianavaliabilityUpdate(CA, AOFC, -20, hours, 3, i, j)
                return stage
            if j == (len(AOFC[i]) - 1):
                return stage + 1

    def addOne(self, timetableObj, timeindexes, ca, aofc, day, stage, task, repeat, hours, i, type):
        day = self.validDay(timeindexes, day, 10, ca, task, hours, 0)
        for j in range(repeat):
            self.addToTable(timetableObj, timeindexes, day, i, ca[i][2][stage], type)
            self.comedianavaliabilityUpdate(ca, aofc, day, stage, 3.2, i, 0)
            stage += 1
            if type == "main":
                day += 1
                day = self.validDay(timeindexes, day, 10, ca, task, hours, 0)
        return day

    def comedianavaliabilityUpdate(self, CA, AOFC, day, hours, task, i, j):
        if task != 3.2:
            comedianInfoArray = [x for x in CA if AOFC[i][j] in x][0]
            index = CA.index(comedianInfoArray)
        if task == 1:
            CA[index][1] = CA[index][1] + 1
            if CA[index][2] == -20:
                CA[index][2] = day
            else:
                CA[index][3] = day
        if task == 2:
            CA[index][1] = CA[index][1] + int(hours)
            for k in range(4):
                if CA[index][2][k] == -20 or CA[index][2][k] == day:
                    CA[index][2][k] = day
                    CA[index][3][k] = CA[index][3][k] + hours
                    break
        # currently just updating their counter
        if task == 3:
            CA[index][1] = CA[index][1] + int(hours)
            for k in range(4):
                if CA[index][2][k] == -20:
                    CA[index][2][k] = i
                    break
        if task == 3.2:
            CA[i][3][hours] = day

        return None

    # -20 is the same as saying 'null' or it has no value for that yet
    # task 1 [[name,counter,day1, day2],...]
    # task 2 and 3 [[name,totalHours, day, hours]] - if schedule more than 2 days, wont exceed 2h a day
    def comedianSchedulingArray(self, task):
        CA = []  # this will be our comedianavaliability array
        for j in range(len(self.comedian_List)):
            availabilty = []
            availabilty.append(self.comedian_List[j].name)
            availabilty.append(0)
            if task == 1:
                availabilty.append(-20)
                availabilty.append(-20)
            elif task == 2:
                availabilty.append([-20, -20, -20, -20])
                availabilty.append([0, 0, 0, 0])
            CA.append(availabilty)
        return CA

    def makeAOFC(self, showType):
        AOFC = [*range(len(self.demographic_List))]

        for i in range((len(self.demographic_List))):
            comediansForDemographic = []
            demo_set = set(self.demographic_List[i].topics)
            for j in range(len(self.comedian_List)):
                if demo_set.issubset(self.comedian_List[j].themes) and showType == "Main":
                    comediansForDemographic.append(self.comedian_List[j].name)
                if demo_set.isdisjoint(self.comedian_List[j].themes) == False and showType == "Test":
                    comediansForDemographic.append(self.comedian_List[j].name)
            AOFC[i] = comediansForDemographic
        return AOFC

    def daytranslator(self, dayindex):
        switcher = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
        }
        return switcher.get(dayindex)

    # This simplistic approach merely assigns each demographic and comedian to a random, iterating through the timetable.
    def randomMainSchedule(self, timetableObj):

        sessionNumber = 1
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        dayNumber = 0
        for demographic in self.demographic_List:
            comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

            timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

            sessionNumber = sessionNumber + 1

            if sessionNumber == 6:
                sessionNumber = 1
                dayNumber = dayNumber + 1

    # This simplistic approach merely assigns each demographic to a random main and test show, with a random comedian, iterating through the timetable.
    def randomMainAndTestSchedule(self, timetableObj):

        sessionNumber = 1
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        dayNumber = 0
        for demographic in self.demographic_List:
            comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

            timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

            sessionNumber = sessionNumber + 1

            if sessionNumber == 11:
                sessionNumber = 1
                dayNumber = dayNumber + 1

        for demographic in self.demographic_List:
            comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

            timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "test")

            sessionNumber = sessionNumber + 1

            if sessionNumber == 11:
                sessionNumber = 1
                dayNumber = dayNumber + 1
