
from utilmy import log, log2
def help():
    """function help
    Args:
    Returns:

    """
    from utilmy import help_create
    print( help_create(MNAME) )



#############################################################################################
def test_all() -> None:
    """function test_all
    """
    log(MNAME)
    test1()




###################################################################################################
if __name__ == "__main__":
    import fire

    fire.Fire()


