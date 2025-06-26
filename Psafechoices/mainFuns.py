"""
Tools to perform Monte-Carlo analysis and explore the variability of safety perceptions
in different cities with different groups of people

@author: ptzouras
National Technical University of Athens
"""
import pandas as pd
import numpy as np
# import os
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from scipy.stats import ttest_rel

#### PROBLEM
# os.chdir("/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/Psafechoices")
from calc import coeffUpd, levelEst

color_dict = {
        '1: Urban road with sidewalk less than 1.5 m wide': '#E31A1C',
        '2: Urban road with sidewalk more than 1.5 m wide': '#FF7F00',
        '3: Urban road with cycle lane': '#0000FF',
        '4: Shared space': '#1DD083',
        'unknown type': 'grey'}

# define transport modes for which perceived safety will be estimated
modes = ['car', 'ebike', 'escoot', 'walk']

def linksPsafe_import(scenario_path):
    """
    Loads the network shapefile for the specified city and version.

    Parameters
    ----------

    scenario_path : str
        the path of the links file

    Returns
    -------
    geopandas.GeoDataFrame
        GeoDataFrame of the network links.
    """
    
    # scenario_path = os.path.join(
    #     root_dir,
    #     f"scenario{city}",
    #     f"baseNetwork{version}",
    #     f"baseNetwork{city}Links{specific_version}.shp"
    # )
    
    links = gpd.read_file(scenario_path)
    
        # Define a mapping between old suffixes and new readable suffixes
    mode_suffix_map = {
        'ca': 'car',
        'eb': 'ebike',
        'es': 'escoot',
        'wa': 'walk'
    }
    
    # Build the renaming dictionary for both LatPsafe and LevPsafe columns
    rename_columns = {
        f'LatPsafe{old}': f'LatPsafe{new}'
        for old, new in mode_suffix_map.items()
    }
    rename_columns.update({
        f'LevPsafe{old}': f'LevPsafe{new}'
        for old, new in mode_suffix_map.items()
    })
    
    # Apply the renaming
    links = links.rename(columns=rename_columns)
    
    return links

def modelPsafe_import(models_path):
    
    """
    Import and prepare mode-specific safety model coefficients for a given city and version.
    
    This function loads the `psafe_models.csv` file containing coefficients,
    renames and sets the appropriate index, and applies coefficient updates 
    via the `coeffUpd()` function.
    
    Parameters
    ----------
    models_path : str
        The path where the models are contained.
    
    version : str
        Model version identifier used to locate the appropriate subdirectory 
        (e.g., "_v1", "_2025", "_baseline").
    
    Returns
    -------
    pd.DataFrame
        A DataFrame of updated coefficients for the psafe model.
        
    """

    cf = pd.read_csv(models_path)
    cf = cf.rename(columns={'Unnamed: 0': 'coeffs'})
    cf = cf.set_index('coeffs')
    cf = coeffUpd(cf) # Please check all the coefficients
    return cf

def odds_mc(cf, typ, tmode, level = None, n_sim=1000, seed=None):
    
    """
    Compute Monte Carlo simulated odds based on a given perceived safety model
    
    This function simulates the odds of psafe being less than or equal to safe level,
    for a given traveller type using normal distributions for uncertain coefficients.
    
    Parameters
    ----------
    cf : pd.DataFrame
        A DataFrame containing coefficient values and standard deviations. 
        Rows are coefficient names (e.g., 'type1', 'sd.type1', 'kappa.0', etc.), 
        columns are transport modes (e.g., 'car', 'bike').
        
    typ : str
        Infrastructure type: 'type1', 'type2', 'type4'. 
    
    tmode : str
        The transport mode column in `cf` to use: 'car', 'ebike', 'escoot', 'walk'
    
    level : int or None, optional
        the safety level used used as threshold
        if None, then the estimation is done based on level 6
    
    n_sim : int, optional
        Number of Monte Carlo simulations to perform. Default is 1000.
    
    seed : int or None, optional
        Random seed for reproducibility. If None, randomness is not seeded.
    
    Returns
    -------
    np.ndarray
        A 1D array of simulated odds values computed as:
        `odds = exp(kappa - type_coeff - other terms)`
        where type_coeff is a sampled coefficient depending on `typ`.
    
    Notes
    -----
    - The function uses normal distributions to sample uncertain type coefficients.
    - Additional fixed terms (like 'pav' and 'cross1') are added to the exponent.
    
    Examples
    --------
    >>> odds_mc(cf, typ="type1", tmode="car", kappa="kappa.0", n_sim=10000, seed=42)
    array([1.23, 1.45, 1.01, ..., 1.67])
    """
    
    if level == 1: kappa = "kappa.0"
    elif level == 2: kappa = "kappa.1"
    elif level == 3: kappa = "kappa.2"
    elif level == 4: kappa = "kappa.3"
    elif level == 5: kappa = "kappa.5"
    else: kappa = "kappp.6"
    
    
    if seed is not None:
        np.random.seed(seed)

    # Initialize type flags
    type_1 = int(typ == "type1")
    type_2 = int(typ == "type2")
    type_4 = int(typ == "type4")

    # Extract mean and std for each relevant coefficient
    means = {
        "type1": cf.loc["type1", tmode],
        "type2": cf.loc["type2", tmode],
        "type4": cf.loc["type4", tmode],
        kappa: cf.loc[kappa, tmode]
    }
    stds = {
        "type1": cf.loc["sd.type1", tmode],
        "type2": cf.loc["sd.type2", tmode],
        "type4": cf.loc["sd.type4", tmode],
        kappa: 0.0  # Assume no uncertainty in kappa.4 unless sd is given
    }

    # Sample from normal distributions
    type1_samples = np.random.normal(means["type1"], stds["type1"], n_sim)
    type2_samples = np.random.normal(means["type2"], stds["type2"], n_sim)
    type4_samples = np.random.normal(means["type4"], stds["type4"], n_sim)
    kappa_samples = np.full(n_sim, means[kappa])  # or sample if needed

    exponent = kappa_samples - (
        type1_samples * type_1 +
        type2_samples * type_2 +
        type4_samples * type_4
    )
    # print(exponent)
    exponent = exponent + cf.loc["pav", tmode] + cf.loc["cross1", tmode]
    odds = np.exp(exponent) # The odds functions

    return odds  # can return mean, quantiles, etc. if preferred


def plotOdds(tmode, cf1, cf2, xlim = None, l = 4, n = 1000):
    
    """
    
    This function directly estimates the odds of two cities and plots their distributions
        
    This function visualizes the distributions of simulated odds for four 
    predefined infrastructur types ("type1", "type2", "type4"), comparing perceptions of residents coming from two cities.
    For "type3", it plots vertical lines at the mean of the simulated odds instead of a histogram.
    
    Parameters
    ----------
    tmode : str
        The transport mode to simulate (e.g., "car", "bike", "pt").
    
    cf1 : object
        The model sets (coefficients) of city 1, used as input to the `odds_mc` function.
    
    cf_Munich : object
        The model sets (coefficients) of city 1, used as input to the `odds_mc` function.
    
    xlim : int or float, optional
        Upper limit for the x-axis (odds values). Determines bin range for histograms.
        If None, function may raise an error unless xlim is explicitly provided.
    
    l : int or float, default=4
        Threshold safety level used in the `odds_mc` simulation,
        so it is the chance of psafe being equal to or lower that the defined  threshold
    
    n : int, default=1000
        Number of Monte Carlo simulations to run per transport mode
    
    Returns
    -------
    None
        The function displays a matplotlib figure with histograms and vertical mean lines
        for simulated odds. It does not return any object.
    
    Notes
    -----
    - The function depends on an external `odds_mc()` function which is defined in the mainFuns.py
    """
    

    def returnLabel(x, typ, city):
        maxX = np.max(x)
        meanX = np.mean(x)
        label_text = f"{city}, {typ} (mean={meanX:.2f}, max={maxX:.2f})"
        return label_text
    
    plt.figure(figsize=(10, 6), dpi = 500)

    typex = ['type1', 'type2', 'type3','type4']
    colors = ['#E31A1C', '#FF7F00', '#0000FF', '#1DD083']
    light_colors = ['#FCA6A8', '#FFCB99', '#99CCFF', '#B5F0D5']
    
    bins = np.arange(0, xlim + 5, 5)  # [0, 100, 200, ..., 2000]

    for i, typ in enumerate(typex): 
        if typ == "type3":
            odds_samples = odds_mc(cf1, 'type3', tmode, level = l, n_sim = n)
            mean_val = np.mean(odds_samples)
            label_text = returnLabel(odds_samples, 'Athens', typ)
            plt.axvline(mean_val, label= label_text, alpha=1, color = colors[i])
        else:
            odds_samples = odds_mc(cf1, typ, tmode, level = l, n_sim = n)
            label_text = returnLabel(odds_samples, 'Athens', typ)
            
            sns.histplot(odds_samples, kde=False, color = colors[i], label= label_text, bins = bins,
                         alpha = 1)
            
            # sns.kdeplot(odds_samples, label= label_text, alpha=1, color = colors[i])
            
    for i, typ in enumerate(typex): 
        if typ == "type3":
            odds_samples = odds_mc(cf2, 'type3', tmode, level = l, n_sim = n)
            mean_val = np.mean(odds_samples)
            label_text = returnLabel(odds_samples, 'Munich', typ)
            plt.axvline(mean_val, label= label_text, alpha=1, linestyle = '--', color = colors[i])
        else:
            odds_samples = odds_mc(cf2, typ, tmode, level = l, n_sim = n)
            label_text = returnLabel(odds_samples, 'Munich', typ)
            
            sns.histplot(odds_samples, kde=False, color = light_colors[i], label= label_text, bins = bins,
                         alpha = 0.8)
            
            # sns.kdeplot(odds_samples, label= label_text, alpha=1, linestyle = '--', color = colors[i]) 

    plt.title(f"Monte-Carlo simulated odds for psafe being less than or equal to {l}, {tmode}")
    plt.xlim([0, xlim])
    plt.xlabel("Odds")
    plt.ylabel("Frequency (max 1000 draws)")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

def score_mc(links, cf, modes = ['car', 'ebike', 'escoot', 'walk'],  
                           runs=100, seed=None, out = True, 
                           city = 'Athens', model = 'Athens_v1'):
    """
    Simulates perceived safety levels for multiple transport modes across multiple runs,
    drawing from normal distributions defined by standard deviations of random beta variables 
    that are related to infrastrcture typ

    Parameters
    ----------
    links : pd.DataFrame
        The links dataframe containing infrastructure type, base latent safety scores, and geometry.
        
    cf : pd.DataFrame
        Coefficients dataframe with mean and standard deviation values per mode.
        
    modes : list of str, default is ['car', 'ebike', 'escoot', 'walk']
        List of transport modes to simulate.
        
    runs : int, default=100
        Number of Monte Carlo runs to perform.
        
    seed : int or None
        Random seed for reproducibility.
        
    out : bool, defualt is True
        If true, it create a barplot with the psafe score distribution per transport mode
        
    city : str, default is Athens
        The city network for which estimations are performed.
        This definition are not necessary, if out is False
    
    model : str, default is Athens_v1
        The model based on which estimations are performed.
        This definition are not necessary, if out is False

    Returns
    -------
    pd.DataFrame
        A long-form dataframe with columns: 'osm_id', 'geometry', 'inf', 'run', and one column per mode
        for perceived safety level (Likert scale 1–7).
    """
    if seed is not None:
        np.random.seed(seed)

    results = []

    for run in range(1, runs + 1):
        for m in modes:
            # Define and sample betas
            beta_stats = {
                '1: Urban road with sidewalk less than 1.5 m wide': {'mean': 0, 'std': cf.loc['sd.type1', m]},
                '2: Urban road with sidewalk more than 1.5 m wide': {'mean': 0, 'std': cf.loc['sd.type2', m]},
                '3: Urban road with cycle lane': {'mean': 0, 'std': 0},
                '4: Shared space': {'mean': 0, 'std': cf.loc['sd.type4', m]},
            }
            # the concept is that in the already estimated levels, we add the standard deviation as an extra error
            sampled_betas = {
                inf_type: np.random.normal(stats['mean'], stats['std'])
                for inf_type, stats in beta_stats.items()
            }

            links['msd'] = links['inf'].map(sampled_betas)
            links[f'LatPsafe{m}_upd'] = links[f'LatPsafe{m}'] + links['msd'] # the calculation is done here
            # but it required the re-estimation of perceived safety
            links[f'LevPsafe{m}_upd'] = links[f'LatPsafe{m}_upd'].apply(lambda x: levelEst(x, cf, m))

        # Store the results for this run
        df_run = links[['osm_id', 'geometry', 'inf'] + [f'LevPsafe{m}_upd' for m in modes]].assign(run=run)
        results.append(df_run)
        
    df = pd.concat(results, ignore_index=True)
        
    if out: plotScores_mc(df, city, model)

    return df

def plotScores_mc(df, city, model):
    """
    It is a plotting function to compare results
    """
    likert_levels = list(range(1, 8))
    inf_types = df['inf'].unique()
    
    r = max(df.run)

    for m in modes:
        col = f'LevPsafe{m}_upd'
        
        data = []
        
        for inf in inf_types:
            subset = df[df['inf'] == inf][col]
            total = len(subset)
            level_counts = subset.value_counts().reindex(likert_levels, fill_value=0)
            level_percents = (level_counts / total * 100).values
            for level, pct in zip(likert_levels, level_percents):
                    data.append({'Level': level, 'Percent': pct, 'Infrastructure': inf})
                    
            
        plot_df = pd.DataFrame(data)
        plt.figure(figsize=(10, 6), dpi=500)
        sns.barplot(data=plot_df, x='Level', y='Percent', hue='Infrastructure', 
                    palette={k: color_dict.get(k, 'grey') for k in plot_df['Infrastructure'].unique()})
        plt.title(f'city: {city}, model: {model}, mode: {m}, runs: {r}', fontsize=12)
        plt.xlabel('Perceived safety level (1 to 7)')
        plt.ylabel('Percentage (%)')
        plt.ylim(0, 100)
        plt.grid(True)
        plt.legend(title='Infrastructure Type')
        # plt.legend(title='Infrastructure Type', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

def betas_sim(cf, m, seed):
    
    """
        Simulate random beta values for different infrastructure types for a given mode.
        
        This function samples from normal distributions with specified means (0) and
        standard deviations derived from a coefficient DataFrame (`cf`).
        
        Parameters
        ----------
        cf : pandas.DataFrame
            A DataFrame containing standard deviations different infrastructure types and modes. 
            Indexed by coefficient type, with modes as columns.
            
        m : str
            The transport mode
        
        seed : int or None
            A random seed for reproducibility
        
        Returns
        -------
        sampled_betas : dict
            A dictionary mapping with betas per infrastructure type
        
        Notes
        -----
        - Infrastructure types are identified by keys like:
          '1: Urban road with sidewalk less than 1.5 m wide'
        - The beta value for '3: Urban road with cycle lane' is always 0 (i.e., no uncertainty).
        """
    
    if seed is not None:
        np.random.seed(seed)
    
    beta_stats = {'1: Urban road with sidewalk less than 1.5 m wide': {'mean': 0, 'std': cf.loc['sd.type1', m]},
                  '2: Urban road with sidewalk more than 1.5 m wide': {'mean': 0, 'std': cf.loc['sd.type2', m]},
                  '3: Urban road with cycle lane': {'mean': 0, 'std': 0},
                  '4: Shared space': {'mean': 0, 'std': cf.loc['sd.type4', m]}}
    
    # the concept is that in the already estimated levels, we add the standard deviation as an extra error
    sampled_betas = {inf_type: np.random.normal(stats['mean'], stats['std'])
                    for inf_type, stats in beta_stats.items()}
    return sampled_betas

def combineLinks(links1, links2):
    """
        This function merges `links1` and `links2` by aligning their rows,
        assuming both have already-matched entries with the same 'id' values.
        It sace very specific columns related to link ID, geometry, infrastructure
        type, and Latent Psafe values (prefixed with suffixes '_1' and '_2').
    """
    
    # TODO: this functions may not be used with other networks
    
    # this part combines the two link files
    links1 = links1.dropna(subset=["id"]) # links have been estimated based on mean values
    links2 = links2.dropna(subset=["id"])
    
    df = pd.concat([links1.add_suffix('_1'), links2.drop(columns = ['id', 'geometry', 'inf']).add_suffix('_2')], axis=1)
    df = df.rename(columns = {'id_1': 'id', 'geometry_1': 'geometry', 'inf_1': 'inf'})
    # it creates a new df with only the osm_id, geometry and psafe evaluations
    cols_to_keep = ["id", "geometry", "LatPsafe", "inf"]
    df = df[[col for col in df.columns if any(key in col for key in cols_to_keep)]]
    return df

def compute_diff_stats(x1_all, x2_all):
    """
        Compute mean difference, standard deviation, t-statistic, and p-value
        from two lists of Series (x1 and x2 values across runs).
    """
    # Concatenate all runs into one Series
    x1_flat = pd.concat(x1_all)
    x2_flat = pd.concat(x2_all)

    diff = x1_flat - x2_flat
    mean_diff = diff.mean()
    std_diff = diff.std(ddof=1)

    # Paired t-test
    t_stat, p_value = ttest_rel(x1_flat, x2_flat)

    return mean_diff, std_diff, t_stat, p_value

def score_diff(links1, links2, cf1, cf2,
              modes = ['car', 'ebike', 'escoot', 'walk'], runs=100, seed = None):
    
    """
        Compare safety level scores between two link datasets using Monte Carlo simulation.
        Examination of their significance.
        
        Parameters
        ----------
        links1 : pandas.DataFrame
            First dataset of links with latent safety scores
        
        links2 : pandas.DataFrame
            Second dataset of links with latent safety scores (alternative scenario).
        
        cf1 : pandas.DataFrame
            Coefficients and thresholds used for scoring `links1`. Should contain standard deviations
            for infrastructure types indexed by labels like 'sd.type1', with modes as columns.
        
        cf2 : pandas.DataFrame
            Coefficients and thresholds used for scoring `links2`, structured the same as `cf1`.
        
        modes : list of str, optional
            List of transport modes to evaluate. Default includes ['car', 'ebike', 'escoot', 'walk'].
        
        runs : int, optional
            Number of Monte Carlo simulation runs to perform per link and mode. Default is 100.
        
        seed : int or None, optional
            Random seed for reproducibility. If None, results are not deterministic.
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with one row per link and mode combination, containing:
            - 'osm_id': Link identifier
            - 'mode'  : Transport mode
            - 'mean'  : Mean difference in estimated safety levels across runs
            - 'std'   : Standard deviation of the differences
            - 't_stat': Paired t-test statistic
            - 'p_value': P-value from the t-test
            - 'geometry': Original geometry of the link (useful for mapping)
        
        Notes
        -----
        - Assumes that links in `links1` and `links2` are aligned and comparable.
        - The comparison is made pairwise (per link and per mode), based on sampled variations in latent scores.
    """
    

    df = combineLinks(links1, links2)
    
    results = []

    for l, pr in df.groupby("id"):  # much faster than repeated df.loc lookups
        for m in modes:
            base1 = pr[f'LatPsafe{m}_1'].values
            base2 = pr[f'LatPsafe{m}_2'].values
            inf_vals = pr['inf'].values
            geometry = pr['geometry'].values

            x1_all = []
            x2_all = []

            for _ in range(runs):
                sampled_betas1 = betas_sim(cf1, m, seed) # collect sample betas for inf from a normal distribution
                sampled_betas2 = betas_sim(cf2, m, seed)

                inf_beta1 = np.vectorize(sampled_betas1.get)(inf_vals) 
                inf_beta2 = np.vectorize(sampled_betas2.get)(inf_vals)

                x1_vals = base1 + inf_beta1 # update the psafe scores based on the inf type
                x2_vals = base2 + inf_beta2

                x1 = pd.Series([levelEst(x, cf1, m) for x in x1_vals]) # estimate the psafe levels based on kappa thresholds
                x2 = pd.Series([levelEst(x, cf2, m) for x in x2_vals])

                x1_all.append(x1)
                x2_all.append(x2)

            # Compute stats
            mean_diff, std_diff, t_stat, p_value = compute_diff_stats(x1_all, x2_all) # estimate descriptive stats of the difference

            results.append({'osm_id': l, 'mode': m, 'mean': mean_diff, 'std': std_diff,
                            't_stat': t_stat, 'p_value': p_value, 'geometry': geometry})
    
    return pd.DataFrame(results)



