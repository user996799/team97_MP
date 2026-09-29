from lime.lime_text import LimeTextExplainer
explainer=LimeTextExplainer(class_names= ["real","fake"])
no_of_words=5
def explanation (text,model,no_of_words=5):
  #in the method explain_instance the inputs are the text
  #then the models prediction on changing each word in sentence
  #last one is how many of the highest probabilty words that
  #we want to have


  reasoning = explainer.explain_instance(
    text,
    model.predict_proba,
    num_features = min(no_of_words,len(text.strip().split("")))
  )
  list=[]
  for word,weight in  reasoning.as_list():
    list.append(
        {
            "word":word,
            "weight":weight,
            "prediction":  "towards real" if weight>0 else "towards fake"
        }
      )
  return list

  def analyze (text,model,no_of_words=5):
    if not text or not text.strip():
        return {
            "prediction": None,
            "confidence": None,
            "explanation": [],
            "error": "no text provided",
        }
        no_of_words = min(no_of_words,len(text.strip().split("")))
        prediction=model.predict([text])[0]
        confidence=float(max(model.predict_proba([text])[0].max()))
        return { "prediction":prediction,
              "confidence":confidence,
              "explanation":explanation(text,model,no_of_words)
              }