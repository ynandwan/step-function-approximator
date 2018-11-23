MIN = -1.0*float('inf')
MAX = float('inf')

def get_one_step_approximator(error_type, points):
    if error_type == 0:
        return MSESingleStepApproximator(points)
    elif error_type == 1:
        return MAESingleStepApproximator(points)


class MAESingleStepApproximator(object):
    def __init__(self, points):
        self.points = points 
        self.length = len(self.points)
        self.last_i = -1
        self.last_j = -1
        self.last_min = MAX 
        self.last_max  = MIN 

    #get single step approximator for points between i and j , inclusive of both
    #valid range for i,j = 0 ... (self.length-1)
    def get_approximation(self,i,j):
        this_point = None
        if ((self.last_i == i) and (j == self.last_j + 1)):
            this_point = self.points[j]
        elif ((self.last_j == j) and (i == self.last_i -1)):
            this_point = self.points[i]

        if this_point is not None:
            self.last_min = min(self.last_min,this_point.y)
            self.last_max = max(self.last_max,this_point.y)
            self.last_i = i
            self.last_j = j
            return (0.5*(self.last_max - self.last_min) , 0.5*(self.last_max + self.last_min))
        else:
            #need to perform O(j-i) operation..
            self.last_min = MAX
            self.last_max = MIN
            for ind in range(i,j+1):
                this_point = self.points[ind]
                self.last_min = min(self.last_min,this_point.y)
                self.last_max = max(self.last_max,this_point.y)
            #
            self.last_i = i
            self.last_j = j
            return (0.5*(self.last_max - self.last_min) , 0.5*(self.last_max + self.last_min))

    def combine(self,e1,e2):
        return max(e1,e2)

class MSESingleStepApproximator(object):
    def __init__(self,points):
        self.points = points
        self.length = len(self.points)
        if self.length > 0:
            self.cum_sum = [self.points[0].y]
            self.cum_sum2 = [self.points[0].y**2]
            for i in range(1,len(self.points)):
                p = self.points[i]
                self.cum_sum.append(self.cum_sum[i-1]+p.y)
                self.cum_sum2.append(self.cum_sum2[i-1]+p.y**2)
        else: 
            self.cum_sum = []
            self.cum_sum2 = []


    def get_approximation(self,i,j):
        n = j - i + 1
        if i == 0:
            err2 = self.cum_sum2[j] - (self.cum_sum[j]**2)/n
            avg = self.cum_sum[j]/n 
        else:
            sum2 = self.cum_sum2[j] - self.cum_sum2[i-1]
            sum1 = self.cum_sum[j] - self.cum_sum[i-1]
            err2  = 1.0*sum2 - 1.0*(sum1**2)/(1.0*n)
            avg = (1.0*sum1/n)
        #
        return (err2,avg)

    def combine(self,e1,e2):
        return e1 + e2 
