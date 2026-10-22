
def score_role_relevance(job_title, target_roles):
    for role in target_roles:
        if role.lower() in job_title.lower():
            return 25
    
    return 0