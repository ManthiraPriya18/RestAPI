from flask import Flask,jsonify,request

app=Flask(__name__)
recipes = [
    {"id": 1, "name": "Pasta", "ingredients": ["noodles", "sauce"], "time": 30},
    {"id": 2, "name": "Pizza", "ingredients": ["dough", "cheese"], "time": 45}
]
@app.route("/")
def home():
    return "Hello"

@app.route("/recipes",methods=["GET"])
def get_recipe():
    return jsonify(recipes),200


@app.route("/recipes/<int:rec_id>",methods=["GET"])
def get_recipe_id(rec_id):
    recipe=next((r for r in recipes if r['id']==rec_id),None )
    if recipe:
        return jsonify(recipe),200
    return jsonify({"Error":"Recipe Not found"}),404

@app.route("/recipes",methods=["POST"])
def post_recipe():
    data=request.get_json()
    if recipes:
        new_id=recipes[-1]['id']+1
    else:
        new_id=1
    new_recipe={
        "id":new_id,
        "name":data["name"],
        "ingredients":data["ingredients"],
        "time":data["time"]
        
    }
    recipes.append(new_recipe)
    return jsonify(new_recipe),201

@app.route("/recipes/<int:upd_id>",methods=["PUT"])
def update_recipe(upd_id):
    data=request.get_json()
    for recipe in recipes:
        if recipe['id']==upd_id:
            recipe.update(data)
            return jsonify(recipes),200
    return jsonify({"error":"Recipe not found"}),404
@app.route("/recipes/<int:del_id>",methods=["DELETE"])
def del_recipe(del_id):
    global recipes
    orginal_len=len(recipes)
    recipes=[r for r in recipes if r["id"]!=del_id]
    if orginal_len>len(recipes):
        return jsonify({"Message":"Suceesfully deleted"})
    return jsonify({"Error":"Not found"})

if __name__ == "__main__":
    app.run(debug=True)