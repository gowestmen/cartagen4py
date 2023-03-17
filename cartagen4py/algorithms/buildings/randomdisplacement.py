# This is an implementation of the random building displacement algorithm

import random, math, shapely

class BuildingDisplacementRandom:
    """
        Initialize random displacement object, with default length displacement factor and number of iterations per building
    """
    def __init__(self, max_trials=25, max_displacement=0.0002):
        self.MAX_TRIALS = max_trials
        self.MAX_DISPLACEMENT = max_displacement

    def displace(self, buildings, roads, rivers):
        # Calculating the mean rate of overlapping buildings with othe buildings, roads and rivers
        # It represents the mean congestion of buildings within the building block
        rate_mean = self.__get_buildings_overlapping_rate_mean(buildings, roads, rivers)

        # Starting trial count
        trial = 0
        # Launching the loop which will displace buildings randomly as long as the rate mean is above 0 and the max trial count is not exceeded
        while rate_mean > 0 and trial <= self.MAX_TRIALS:
            # Selecting a random building index
            random_index = random.randint(0, len(buildings) - 1)
            random_building = buildings[random_index]
            # Checking if that building is overlapping
            if (self.__get_building_overlap(random_building, buildings, roads, rivers) != 0):
                # Selecting a random angle (0-360)
                random_angle = random.uniform(0, 360)
                # Selecting a random lenght (0-max displacement variable)
                random_length = random.uniform(0, self.MAX_DISPLACEMENT)
                # Calculate displacement for x and y
                dx = math.cos(random_angle) * random_length
                dy = math.sin(random_angle) * random_length

                # Translating the building with the random values
                translated = shapely.affinity.translate(random_building, dx, dy)
                buildings[random_index] = translated

                # Calulcating the new rate mean
                new_rate_mean = self.__get_buildings_overlapping_rate_mean(buildings, roads, rivers)

                # If the new rate mean is equal or higher, we cancel the translation
                if (new_rate_mean >= rate_mean):
                    buildings[random_index] = random_building
                    trial += 1
                # Else, resetting the trial count and updating the rate mean
                else:
                    rate_mean = new_rate_mean
                    trial = 0
                print(rate_mean)
                
        return buildings

    # Calculate the overlapping mean rate
    def __get_buildings_overlapping_rate_mean(self, buildings, roads, rivers):
        # If no buildings are provided, returns 0
        if len(buildings) == 0:
            return 0
        mean = 0
        nb = 0

        # For each building, calculating the area overlapping other buildings, roads and rivers depending on a distance value
        for b in buildings:
            mean += self.__get_building_overlap(b, buildings, roads, rivers)
            nb += 1
        # Calculating the mean area
        if nb != 0:
            mean = mean/nb

        return mean

    # Calculate the area of overlapping between buildings, roads and rivers
    def __get_building_overlap(self, processed_building, buildings, roads, rivers):
        distance = 0.0001
        geometry = None

        # For each buildings...
        for building in buildings:
            # Checking if it's not the same building
            if building != processed_building:
                geometry = self.__get_overlapping_geometries(processed_building, building, distance, geometry)
        
        # For each road section
        for road in roads:
            geometry = self.__get_overlapping_geometries(processed_building, road, distance, geometry)

        # For each river section
        for river in rivers:
            geometry = self.__get_overlapping_geometries(processed_building, river, distance, geometry)

        # Returning the area of the geometry if it exists
        if (geometry is None) or (geometry.is_empty == True) or (geometry.area == 0):
            return 0
        else:
            return geometry.area

    # Calculate the geometry of the intersection between a geographic object and a building if the building is closer to this object than a defined value
    def __get_overlapping_geometries(self, processed_building, obj, distance, geometry):
        # If the building is closer to the object than the distance variable
        if processed_building.dwithin(obj, distance):
            # Creating the intersection between the buffer around the object and the building
            intersection = shapely.intersection(shapely.buffer(obj, distance), processed_building)
            # If the geometry is empty, return the intersection...
            if geometry is None:
                return intersection
            # Else, returning the union between the intersection and the existing geometry
            else:
                return geometry.union(intersection)
        else:
            return geometry