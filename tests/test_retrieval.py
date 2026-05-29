from app.retrieval import retrieve_relevant_schemes

def test_retrieval_pudhumai_penn():
    # Search for pudhumai penn
    results = retrieve_relevant_schemes("Explain Pudhumai Penn scheme")
    
    # Must return results
    assert len(results) > 0
    
    # The top result must be the Pudhumai Penn scheme
    assert results[0]["id"] == "pudhumai_penn"
    assert "https://tnsocialwelfare.tn.gov.in" in results[0]["official_url"]

def test_retrieval_cmchis():
    # Search for health insurance
    results = retrieve_relevant_schemes("What is CMCHIS health cover limit?")
    
    assert len(results) > 0
    assert results[0]["id"] == "cmchis"
    assert "cmchistn.com" in results[0]["official_url"]
