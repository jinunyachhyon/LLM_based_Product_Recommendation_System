from sentence_transformers import SentenceTransformer, util

class LLMRecommender:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Load a lightweight embedding model
        self.model = SentenceTransformer(model_name)

    def rank_products(self, preferences, products):
        """
        Rank products based on semantic similarity with user preferences.
        :param preferences: String representing user preferences.
        :param products: List of product descriptions.
        :return: Ranked list of product descriptions.
        """
        # Step 1: Encode preferences and product descriptions into embeddings
        pref_embedding = self.model.encode(preferences, convert_to_tensor=True)
        product_embeddings = self.model.encode(products, convert_to_tensor=True)

        # Step 2: Compute similarity scores
        scores = util.pytorch_cos_sim(pref_embedding, product_embeddings).squeeze()

        # Step 3: Sort products by similarity scores
        ranked_products = sorted(
            zip(products, scores.tolist()),
            key=lambda x: x[1], reverse=True
        )

        # Step 4: Return only product descriptions in ranked order
        return [product for product, score in ranked_products]