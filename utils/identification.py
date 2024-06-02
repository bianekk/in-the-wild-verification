import numpy as np
import torch

def nearest_tensor(target: torch.Tensor, embeddings: torch.Tensor, thresh: float):
    """
    Finds nearest neighbor for a given speech sample
    Args:
        target -- torch.Tensor of speech sample to identify of shape [E] (embedding size)
        embeddings -- torch.Tensor of model introduced users [N users x M samples x E embedding size]
        thresh -- float, minimum cosine similarity between two users to consider them as a match
    Returns:
        tuple (index, distance)
    """
    # Normalize the tensors
    target_sample_norm = target / target.norm(dim=0)
    user_embeddings_norm = embeddings / embeddings.norm(dim=2, keepdim=True)

    # Compute the cosine similarity
    cosine_similarities = torch.matmul(user_embeddings_norm, target_sample_norm)

    # Find the maximum similarity for each user
    max_similarities, _ = torch.max(cosine_similarities, dim=1)

    # Find the closest user and theirs similarity
    closest_user_index = torch.argmax(max_similarities).item()
    max_similarity_value = torch.max(max_similarities).item()

    if max_similarity_value > thresh:
        return closest_user_index, max_similarity_value
    else:
        print(f"No matching user found")
        return 0, 0

    

if __name__ == "__main__":
    target = torch.rand(128)
    embeddings = torch.rand(10, 15, 128)
    nearest_tensor(target, embeddings, 0.7)