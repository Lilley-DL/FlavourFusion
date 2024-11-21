
from Database import Database

class RecipeManager:
    def __init__(self,db:Database):
        self.db = db

    def getRecipe(self,recipe_id:int):
        #check the input is an int 
        result,row = self.db.get("SELECT * FROM recipes WHERE recipe_id = %s",recipe_id)
        if result:
            recipe = Recipe(row)
            return recipe
        else:
            return False
    
    def getRecipeByName(self, name:str):
        #check the input is a string
        result,row = self.db.get("SELECT * FROM recipes WHERE name = %s",name)
        if result:
            recipe = Recipe(row)
            return recipe
        else:
            return False
        
    def createRecipe(self,name,recipeData):
        sql = "INSERT INTO recipes ('name','data_json') VALUES (%s,%s)"
        values = (name,recipeData)
        return self.db.insert(sql,values) #will pass the result and message back through
        


class Recipe:
    def __init__(self,dbrow):
        self.name = dbrow['name']
        self.data = dbrow['data_JSON']
        self.createdDate = dbrow['created_at']
        self.updatedDate = dbrow['updated_at'] #this might be null 
        self.publisgedDate = dbrow['published_at'] # this might be null