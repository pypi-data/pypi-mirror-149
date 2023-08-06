import sys
from collections import Counter

import matplotlib
import sklearn
import tomotopy as tp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import matplotlib as mpl
import platform
import matplotlib.font_manager as fm
import math
from pyvis.network import Network

class pyTextMinerTopicModel:
    def __init__(self):
        self.name="Topic Model"

    def format_topics_sentences(self, topic_number=20, mdl=None):
        pd.set_option('display.max_columns', None)
        # Init output
        sent_topics_df = pd.DataFrame()

        # we need to make column consistent
        matrix = []
        docs = []
        for d in mdl.docs:
            doc = ''
            for word in d.get_words():
                doc += word[0] + " "
            doc = doc.strip()
            docs.append(doc)

            row = d.get_topics(top_n=topic_number)
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    topic_keywords = ", ".join([word for word, prob in mdl.get_topic_words(topic_num)])
                    sent_topics_df = sent_topics_df.append(
                        pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
                else:
                    break

            a_row = [0.0 for i in range(topic_number)]
            for tup in row:
                for x in range(topic_number):
                    if tup[0] == x:
                        a_row[x] = tup[1]
            #print(str(a_row))
            matrix.append(a_row)

        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(docs)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)

        return(sent_topics_df, matrix)

    def distribution_document_word_count(self, sent_topics_df, df_dominant_topic, result_file='../dist_doc_word_count.png'):
        # The most representative sentence for each topic
        # Display setting to show more characters in column
        pd.options.display.max_colwidth = 100

        sent_topics_sorteddf_mallet = pd.DataFrame()
        sent_topics_outdf_grpd = sent_topics_df.groupby('Dominant_Topic')

        for i, grp in sent_topics_outdf_grpd:
            sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet,
                                                     grp.sort_values(['Perc_Contribution'], ascending=False).head(1)],
                                                    axis=0)

        # Reset Index
        sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)

        # Format
        sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Representative Text"]

        # Show
        print(sent_topics_sorteddf_mallet.head(10))

        # Frequency Distribution of Word Counts in Documents
        # When working with a large number of documents, you want to know how big the documents are as a whole and by topic.
        # Let’s plot the document word counts distribution.
        doc_lens = [len(d) for d in df_dominant_topic.Text]

        # Plot
        figure = plt.figure(figsize=(16, 7), dpi=160)
        plt.hist(doc_lens, bins=1000, color='navy')
        plt.text(750, 100, "Mean   : " + str(round(np.mean(doc_lens))))
        plt.text(750, 90, "Median : " + str(round(np.median(doc_lens))))
        plt.text(750, 80, "Stdev   : " + str(round(np.std(doc_lens))))
        plt.text(750, 70, "1%ile    : " + str(round(np.quantile(doc_lens, q=0.01))))
        plt.text(750, 60, "99%ile  : " + str(round(np.quantile(doc_lens, q=0.99))))

        plt.gca().set(xlim=(0, 200), ylabel='Number of Documents', xlabel='Document Word Count')
        plt.gca().set_ylim([0,200])
        plt.tick_params(size=16)
        plt.xticks(np.linspace(0, 200, 9))
        plt.title('Distribution of Document Word Counts', fontdict=dict(size=22))

        figure.savefig('../dist_doc_word_count.png')
        plt.show()

    def distribution_word_count_by_dominant_topic(self, df_dominant_topic, dominant_topic_number=6, result_file='./result.png'):
        import seaborn as sns
        import matplotlib.colors as mcolors
        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

        x = 3
        y = 2
        if dominant_topic_number > 6:
            x = math.ceil(dominant_topic_number/x)

        #print('X ' + str(x))
        fig, axes = plt.subplots(x, y, figsize=(16, 14), dpi=160, sharex=True, sharey=True)

        for i, ax in enumerate(axes.flatten()):
            df_dominant_topic_sub = df_dominant_topic.loc[df_dominant_topic.Dominant_Topic == i, :]
            doc_lens = [len(d) for d in df_dominant_topic_sub.Text]
            ax.hist(doc_lens, bins=1000, color=cols[i])
            ax.tick_params(axis='y', labelcolor=cols[i], color=cols[i])
            sns.kdeplot(doc_lens, color="black", shade=False, ax=ax.twinx())
            ax.set(xlim=(0, 1000), xlabel='Document Word Count')
            ax.set_ylabel('Number of Documents', color=cols[i])
            ax.set_title('Topic: ' + str(i), fontdict=dict(size=16, color=cols[i]))

        fig.tight_layout()
        fig.subplots_adjust(top=0.90)
        plt.xticks(np.linspace(0, 1000, 9))
        fig.suptitle('Distribution of Document Word Counts by Dominant Topic', fontsize=22)
        fig.savefig(result_file)
        plt.show()

    def word_cloud_by_topic(self, mdl, topic_cloud_result_file='./result.png', topic_number=10):
        #Word Clouds of Top N Keywords in Each Topic
        #Though you’ve already seen what are the topic keywords in each topic, a word cloud
        #with the size of the words proportional to the weight is a pleasant sight.
        #The coloring of the topics I’ve taken here is followed in the subsequent plots as well.
        cols = [color for name, color in mcolors.XKCD_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

        if platform.system() == 'Windows':
            # Window의 경우 폰트 경로
            font_path = 'C:/Windows/Fonts/malgun.ttf'
        elif platform.system() == 'Darwin':
            # for Mac
            font_path = '/Library/Fonts/AppleGothic.ttf'

        cloud = WordCloud(background_color='white',
                          font_path=font_path,
                          collocations=False,
                          width=2500,
                          height=1800,
                          max_words=10,
                          colormap='tab10',
                          color_func=lambda *args, **kwargs: cols[i],
                          prefer_horizontal=1.0)

        x = 3
        y = 2
        if topic_number > 6:
            x = math.ceil(topic_number/(x-1))

        fig, axes = plt.subplots(x, y, figsize=(10, 10), sharex=True, sharey=True)

        for i, ax in enumerate(axes.flatten()):
            ax.set(frame_on=True)
            fig.add_subplot(ax, frameon=True)
            topic_words={}
            for word, prob in mdl.get_topic_words(i):
                topic_words[word]=prob

            if len(topic_words) > 0:
                cloud.generate_from_frequencies(topic_words, max_font_size=300)
                plt.gca().imshow(cloud)
                plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
                plt.gca().axis('on')

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.axis('on')
        plt.margins(x=0, y=0)
        plt.tight_layout()
        fig.savefig(topic_cloud_result_file)
        plt.show()

    def word_count_by_keywords(self, mdl, matrix, topic_keyword_result_file='./topic_keywords.png', topic_number=10):
        from collections import Counter
        data_flat = [w for w_list in matrix for w in w_list]
        counter = Counter(data_flat)

        font_path = ''
        if platform.system() == 'Windows':
            # Window의 경우 폰트 경로
            font_path = 'C:/Windows/Fonts/malgun.ttf'
        elif platform.system() == 'Darwin':
            # for Mac
            font_path = '/Library/Fonts/AppleGothic.ttf'

        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
        plt.rc('axes', unicode_minus=False)

        out = []
        for k in range(mdl.k):
            for word, weight in mdl.get_topic_words(k):
                out.append([word, k, weight, counter[word]])

        df = pd.DataFrame(out, columns=['word', 'topic_id', 'importance', 'word_count'])

        x = 3
        y = 2
        if topic_number > 6:
            x = math.ceil(topic_number/(x-1))

        # Plot Word Count and Weights of Topic Keywords
        fig, axes = plt.subplots(x, y, figsize=(16, 10), sharey=True, dpi=160)
        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
        for i, ax in enumerate(axes.flatten()):
            ax.bar(x='word', height="word_count", data=df.loc[df.topic_id == i, :], color=cols[i], width=0.5, alpha=0.3,
                   label='Word Count')
            ax_twin = ax.twinx()
            ax_twin.bar(x='word', height="importance", data=df.loc[df.topic_id == i, :], color=cols[i], width=0.2,
                        label='Weights')
            ax.set_ylabel('Word Count', color=cols[i])
            ax_twin.set_ylim(0, 0.030);
            ax.set_ylim(0, 3500)
            ax.set_title('Topic: ' + str(i), color=cols[i], fontsize=16)
            ax.tick_params(axis='y', left=False)
            ax.set_xticklabels(df.loc[df.topic_id == i, 'word'], rotation=30, horizontalalignment='right')
            ax.legend(loc='upper left');
            ax_twin.legend(loc='upper right')

        fig.tight_layout(w_pad=2)
        fig.suptitle('Word Count and Importance of Topic Keywords', fontsize=22, y=1.05)

        fig.savefig(topic_keyword_result_file)
        plt.show()

    def sentences_chart(self, mdl, start=0, end=13, sentences_chart_result_file='./sentence_chart.png', topic_number=20):
        font_path = ''
        if platform.system() == 'Windows':
            # Window의 경우 폰트 경로
            font_path = 'C:/Windows/Fonts/malgun.ttf'
        elif platform.system() == 'Darwin':
            # for Mac
            font_path = '/Library/Fonts/Arial Unicode.ttf'

        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
        plt.rc('axes', unicode_minus=False)

        mycolors = [color for name, color in mcolors.TABLEAU_COLORS.items()]

        word_dominanttopic = []
        for k in range(mdl.k):
            print("== Topic #{} ==".format(k))
            topwords = sorted(mdl.get_topic_words(k, top_n=40), key=lambda x: (x[1]), reverse=True)
            #for word, prob in mdl.get_topic_words(k, top_n=20):
            for n, (word, prob) in enumerate(topwords):
                word_dominanttopic.append((word, k))

        print(word_dominanttopic)
        fig, axes = plt.subplots(end-start, 1, figsize=(20, (end-start)*0.95), dpi=160)
        axes[0].axis('off')
        for i, ax in enumerate(axes):
            if i > 0:
                d = mdl.docs[i-1]

                row = d.get_topics(top_n=topic_number)
                # Get the Dominant topic, Perc Contribution and Keywords for each document
                topic_percs = []
                for topic_num, prop_topic in row:
                    topic_percs.append((topic_num,prop_topic))

                ax.text(0.01, 0.5, "Doc " + str(i - 1) + ": ", verticalalignment='center',
                        fontsize=16, color='black', transform=ax.transAxes, fontweight=700)

                # Draw Rectange
                topic_percs_sorted = sorted(topic_percs, key=lambda x: (x[1]), reverse=True)
                ax.add_patch(Rectangle((0.0, 0.05), 0.99, 0.90, fill=None, alpha=1,
                                               color=mycolors[topic_percs_sorted[0][0]], linewidth=2))

                word_pos = 0.06
                for j, (word, topics) in enumerate(word_dominanttopic):
                    if j < 14:
                        ax.text(word_pos, 0.5, word,
                            horizontalalignment='left',
                            verticalalignment='center',
                            fontsize=16, color=mycolors[topics],
                            transform=ax.transAxes, fontweight=700)
                        word_pos += .009 * len(word)  # to move the word for the next iter
                        ax.axis('off')
                ax.text(word_pos, 0.5, '. . .',
                        horizontalalignment='left',
                        verticalalignment='center',
                        fontsize=16, color='black',
                        transform=ax.transAxes)

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.suptitle('Sentence Topic Coloring for Documents: ' + str(start) + ' to ' + str(end-2), fontsize=22, y=0.95, fontweight=700)
        plt.tight_layout()

        fig.savefig(sentences_chart_result_file)
        plt.show()

    # Sentence Coloring of N Sentences
    def topics_per_document(self, mdl, start=0, end=1, topics_per_document='topic_per_document.png', topic_number=10):
        if (end < 1):
            end = len(mdl.docs)

        topic_top3words = []
        dominant_topics = []
        topic_percentages = []

        for k in range(mdl.k):
            print("== Topic #{} ==".format(k))
            for word, prob in mdl.get_topic_words(k, top_n=3):
                topic_top3words.append((k, word))

        for i, idx in enumerate(range(start, end)):
            d = mdl.docs[idx]
            row = d.get_topics(top_n=topic_number)

            # Get the Dominant topic, Perc Contribution and Keywords for each document
            topic_percs = []
            for j, (topic_num, prop_topic) in enumerate(row):
                topic_percs.append(prop_topic)

            #print(topic_percs)
            dominant_topic = sorted(row, key=lambda x: (x[1]), reverse=True)[0][0]
            dominant_topics.append((i, dominant_topic))
            topic_percentages.append(row)

        # Distribution of Dominant Topics in Each Document
        df = pd.DataFrame(dominant_topics, columns=['Document_Id', 'Dominant_Topic'])
        dominant_topic_in_each_doc = df.groupby('Dominant_Topic').size()
        df_dominant_topic_in_each_doc = dominant_topic_in_each_doc.to_frame(name='count').reset_index()

        print(df.head(10))
        print(dominant_topic_in_each_doc)
        # Total Topic Distribution by actual weight

        #topic_weightage_by_doc = pd.DataFrame(topic_percentages)
        topic_weightage_by_doc = pd.DataFrame([dict(t) for t in topic_percentages])
        df_topic_weightage_by_doc = topic_weightage_by_doc.sum().to_frame(name='count').reset_index()

        print(df_topic_weightage_by_doc)

        df_top3words_stacked = pd.DataFrame(topic_top3words, columns=['topic_id', 'words'])
        df_top3words = df_top3words_stacked.groupby('topic_id').agg(', \n'.join)
        df_top3words.reset_index(level=0, inplace=True)

        print(topic_top3words)

        font_path = ''
        if platform.system() == 'Windows':
            # Window의 경우 폰트 경로
            font_path = 'C:/Windows/Fonts/malgun.ttf'
        elif platform.system() == 'Darwin':
            # for Mac
            font_path = '/Library/Fonts/Arial Unicode.ttf'

        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
        plt.rc('axes', unicode_minus=False)

        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=120, sharey=True)

        # Topic Distribution by Dominant Topics
        ax1.bar(x='Dominant_Topic', height='count', data=df_dominant_topic_in_each_doc, width=.5, color='firebrick')
        ax1.set_xticks(range(df_dominant_topic_in_each_doc.Dominant_Topic.unique().__len__()))
        tick_formatter = FuncFormatter(
            lambda x, pos: 'Topic ' + str(x) + '\n' + df_top3words.loc[df_top3words.topic_id == x, 'words'].values[0])
        ax1.xaxis.set_major_formatter(tick_formatter)
        ax1.set_title('Number of Documents by Dominant Topic', fontdict=dict(size=10))
        ax1.set_ylabel('Number of Documents')
        ax1.set_ylim(0, 1000)

        # Topic Distribution by Topic Weights
        ax2.bar(x='index', height='count', data=df_topic_weightage_by_doc, width=.5, color='steelblue')
        ax2.set_xticks(range(df_topic_weightage_by_doc.index.unique().__len__()))
        ax2.xaxis.set_major_formatter(tick_formatter)
        ax2.set_title('Number of Documents by Topic Weightage', fontdict=dict(size=10))

        fig.savefig(topics_per_document)

        plt.show()

    def tSNE(self, mdl, matrix, label, topic_number=10):
        from bokeh.plotting import figure, output_file, show
        from bokeh.models import Label
        from bokeh.io import output_notebook
        import matplotlib.colors as mcolors
        from sklearn.manifold import TSNE

        # Array of topic weights
        arr = pd.DataFrame(matrix).fillna(0).values

        # Dominant topic number in each doc
        topic_num = np.argmax(arr, axis=1)

        # tSNE Dimension Reduction
        tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')
        tsne_lda = tsne_model.fit_transform(arr)

        n_topics = topic_number
        mycolors = np.array([color for name, color in matplotlib.colors.cnames.items()])
        plot = figure(title="t-SNE Clustering of {} " + label + "Topics".format(n_topics),
                      plot_width=900, plot_height=700)

        plot.scatter(x=tsne_lda[:,0], y=tsne_lda[:,1], color=mycolors[topic_num])

        show(plot)

    def pivot_and_smooth(self, df, rows_variable, smooth_value, cols_variable, values_variable):
        """
        Turns the pandas dataframe into a data matrix.
        Args:
            df (dataframe): aggregated dataframe
            smooth_value (float): value to add to the matrix to account for the priors
            rows_variable (str): name of dataframe column to use as the rows in the matrix
            cols_variable (str): name of dataframe column to use as the columns in the matrix
            values_variable(str): name of the dataframe column to use as the values in the matrix
        Returns:
            dataframe: pandas matrix that has been normalized on the rows.
        """
        matrix = df.pivot(index=rows_variable, columns=cols_variable, values=values_variable).fillna(value=0)
        matrix = matrix.values + smooth_value

        normed = sklearn.preprocessing.normalize(matrix, norm='l1', axis=1)

        return pd.DataFrame(normed)

    def make_pyLDAVis(self, mdl, visualization_file='./visualization.html'):
        import pyLDAvis
        topic_term_dists = np.stack([mdl.get_topic_word_dist(k) for k in range(mdl.k)])
        doc_topic_dists = np.stack([doc.get_topic_dist() for doc in mdl.docs])
        doc_topic_dists /= doc_topic_dists.sum(axis=1, keepdims=True)
        doc_lengths = np.array([len(doc.words) for doc in mdl.docs])
        vocab = list(mdl.used_vocabs)
        term_frequency = mdl.used_vocab_freq

        prepared_data = pyLDAvis.prepare(
            topic_term_dists,
            doc_topic_dists,
            doc_lengths,
            vocab,
            term_frequency
        )
        pyLDAvis.save_html(prepared_data, visualization_file)

        #pyLDAvis.save_html(vis_data, visualization_file)

    def hdp_model(self, text_data, save_path):
        mdl = tp.HDPModel(tw=tp.TermWeight.ONE, min_cf=3, rm_top=5)
        index = 0
        for doc in text_data:
            print(str(index) + " : " + str(doc))
            mdl.add_doc(doc)
            index += 1

        mdl.burn_in = 100
        mdl.train(0)
        print('Num docs:', len(mdl.docs), ', Vocab size:', mdl.num_vocabs, ', Num words:', mdl.num_words)
        print('Removed top words:', mdl.removed_top_words)
        print('Training...', file=sys.stderr, flush=True)
        for i in range(0, 1000, 10):
            mdl.train(10)
            print('Iteration: {}\tLog-likelihood: {}\tNum. of topics: {}'.format(i, mdl.ll_per_word, mdl.live_k))

        print('Saving...', file=sys.stderr, flush=True)
        mdl.save(save_path, True)

        topic_num = 0
        # extract candidates for auto topic labeling
        extractor = tp.label.PMIExtractor(min_cf=10, min_df=5, max_len=5, max_cand=10000)
        cands = extractor.extract(mdl)

        # ranking the candidates of labels for a specific topic
        labeler = tp.label.FoRelevance(mdl, cands, min_df=5, smoothing=1e-2, mu=0.25)
        important_topics = [k for k, v in
                            sorted(enumerate(mdl.get_count_by_topics()), key=lambda x: x[1], reverse=True)]
        for k in important_topics:
            if not mdl.is_live_topic(k): continue
            print("== Topic #{} ==".format(k))
            print("Labels:", ', '.join(label for label, score in labeler.get_topic_labels(k, top_n=5)))
            for word, prob in mdl.get_topic_words(k, top_n=10):
                print(word, prob, sep='\t')
            print()
            topic_num+=1
        return (mdl, topic_num)

    def hlda_model(self, text_data, save_path):
        mdl = tp.HLDAModel(tw=tp.TermWeight.ONE, min_cf=3, rm_top=5, depth=2)
        index = 0
        for doc in text_data:
            print(str(index) + " : " + str(doc))
            mdl.add_doc(doc)
            index += 1

        mdl.burn_in = 100
        mdl.train(0)
        print('Num docs:', len(mdl.docs), ', Vocab size:', mdl.num_vocabs, ', Num words:', mdl.num_words)
        print('Removed top words:', mdl.removed_top_words)
        print('Training...', file=sys.stderr, flush=True)
        for i in range(0, 1000, 10):
            mdl.train(10)
            print('Iteration: {}\tLog-likelihood: {}\tNum. of topics: {}'.format(i, mdl.ll_per_word, mdl.live_k))

        print('Saving...', file=sys.stderr, flush=True)
        mdl.save(save_path, True)

        # extract candidates for auto topic labeling
        extractor = tp.label.PMIExtractor(min_cf=10, min_df=5, max_len=5, max_cand=10000)
        cands = extractor.extract(mdl)

        # ranking the candidates of labels for a specific topic
        labeler = tp.label.FoRelevance(mdl, cands, min_df=5, smoothing=1e-2, mu=0.25)
        important_topics = [k for k, v in
                            sorted(enumerate(mdl.get_count_by_topics()), key=lambda x: x[1], reverse=True)]
        for k in important_topics:
            if not mdl.is_live_topic(k): continue
            print("== Topic #{} ==".format(k))

            children_ids = mdl.children_topics(k)
            for id in children_ids:
                print('children topic ' + str(id) + ' ')
            print('\n')

            print("Labels:", ', '.join(label for label, score in labeler.get_topic_labels(k, top_n=5)))
            for word, prob in mdl.get_topic_words(k, top_n=10):
                print(word, prob, sep='\t')
            print()
        return mdl

    def ct_model(self, text_data, save_path, topic_number=20, topic_network_result='./topic_network.html'):
        mdl = tp.CTModel(tw=tp.TermWeight.IDF, min_df=5, rm_top=40, k=topic_number)
        index = 0
        for doc in text_data:
            print(str(index) + " : " + str(doc))
            mdl.add_doc(doc)
            index += 1

        mdl.train(0)

        # Since we have more than ten thousand of documents,
        # setting the `num_beta_sample` smaller value will not cause an inaccurate result.
        mdl.num_beta_sample = 5
        print('Num docs:{}, Num Vocabs:{}, Total Words:{}'.format(
            len(mdl.docs), len(mdl.used_vocabs), mdl.num_words
        ))
        print('Removed Top words: ', *mdl.removed_top_words)

        # Let's train the model
        for i in range(0, 1000, 20):
            print('Iteration: {:04}, LL per word: {:.4}'.format(i, mdl.ll_per_word))
            mdl.train(20)
        print('Iteration: {:04}, LL per word: {:.4}'.format(1000, mdl.ll_per_word))

        mdl.summary()
        print('Saving...', file=sys.stderr, flush=True)
        mdl.save(save_path, True)

        # Let's visualize the result
        g = Network(width=800, height=800, font_color="#333")
        correl = mdl.get_correlations().reshape([-1])
        correl.sort()
        top_tenth = mdl.k * (mdl.k - 1) // 10
        top_tenth = correl[-mdl.k - top_tenth]

        for k in range(mdl.k):
            label = "#{}".format(k)
            title = ' '.join(word for word, _ in mdl.get_topic_words(k, top_n=6))
            print('Topic', label, title)
            g.add_node(k, label=label, title=title, shape='ellipse')
            for l, correlation in zip(range(k - 1), mdl.get_correlations(k)):
                if correlation < top_tenth: continue
                g.add_edge(k, l, value=float(correlation), title='{:.02}'.format(correlation))

        g.barnes_hut(gravity=-1000, spring_length=20)
        g.show_buttons()
        g.show(topic_network_result)

    def visualize_ct_model(self, mdl, topic_network_result='./topic_network.html'):
        # Let's visualize the result
        g = Network(width=800, height=800, font_color="#333")
        correl = mdl.get_correlations().reshape([-1])
        correl.sort()
        top_tenth = mdl.k * (mdl.k - 1) // 10
        top_tenth = correl[-mdl.k - top_tenth]

        for k in range(mdl.k):
            label = "#{}".format(k)
            title = ' '.join(word for word, _ in mdl.get_topic_words(k, top_n=6))
            print('Topic', label, title)
            g.add_node(k, label=label, title=title, shape='ellipse')
            for l, correlation in zip(range(k - 1), mdl.get_correlations(k)):
                if correlation < top_tenth: continue
                g.add_edge(k, l, value=float(correlation), title='{:.02}'.format(correlation))

        g.barnes_hut(gravity=-1000, spring_length=20)
        g.show_buttons()
        g.show(topic_network_result)

    def lda_model(self, text_data, save_path, topic_number=20):
        mdl = tp.LDAModel(tw=tp.TermWeight.ONE, min_cf=3, rm_top=5, k=topic_number)
        index=0
        for doc in text_data:
            print(str(index) + " : " + str(doc))
            mdl.add_doc(doc)
            index+=1


        mdl.burn_in = 100
        mdl.train(0)
        print('Num docs:', len(mdl.docs), ', Vocab size:', mdl.num_vocabs, ', Num words:', mdl.num_words)
        print('Removed top words:', mdl.removed_top_words)
        print('Training...', file=sys.stderr, flush=True)
        for i in range(0, 1500, 10):
            mdl.train(10)
            print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

        print('Saving...', file=sys.stderr, flush=True)
        mdl.save(save_path, True)

        # extract candidates for auto topic labeling
        extractor = tp.label.PMIExtractor(min_cf=10, min_df=5, max_len=5, max_cand=10000)
        cands = extractor.extract(mdl)

        # ranking the candidates of labels for a specific topic
        labeler = tp.label.FoRelevance(mdl, cands, min_df=5, smoothing=1e-2, mu=0.25)
        for k in range(mdl.k):
            print("== Topic #{} ==".format(k))
            print("Labels:", ', '.join(label for label, score in labeler.get_topic_labels(k, top_n=5)))
            for word, prob in mdl.get_topic_words(k, top_n=10):
                print(word, prob, sep='\t')
            print()

        return mdl

    def dmr_model(self, text_data, pair_map, save_path, topic_number=20):
        mdl = tp.DMRModel(tw=tp.TermWeight.ONE, min_cf=3, rm_top=5, k=topic_number)

        index=0
        for doc in text_data:
            print(str(index) + " : " + str(doc))
            year=pair_map[index]
            mdl.add_doc(doc,metadata=year)
            index+=1

        mdl.burn_in = 100
        mdl.train(0)
        print('Num docs:', len(mdl.docs), ', Vocab size:', mdl.num_vocabs, ', Num words:', mdl.num_words)
        print('Removed top words:', mdl.removed_top_words)
        print('Training...', file=sys.stderr, flush=True)
        for i in range(0, 1000, 10):
            mdl.train(10)
            print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

        print(mdl.perplexity)

        print('Saving...', file=sys.stderr, flush=True)
        mdl.save(save_path, True)

        # extract candidates for auto topic labeling
        extractor = tp.label.PMIExtractor(min_cf=10, min_df=5, max_len=5, max_cand=10000)
        cands = extractor.extract(mdl)

        # ranking the candidates of labels for a specific topic
        labeler = tp.label.FoRelevance(mdl, cands, min_df=5, smoothing=1e-2, mu=0.25)
        for k in range(mdl.k):
            print("== Topic #{} ==".format(k))
            print("Labels:", ', '.join(label for label, score in labeler.get_topic_labels(k, top_n=5)))
            for word, prob in mdl.get_topic_words(k, top_n=10):
                print(word, prob, sep='\t')
            print()

        # Init output
        topics_features = pd.DataFrame()
        col_features = []

        for k in range(mdl.k):
            print('Topic #{}'.format(k))
            array_features=[]
            features={}
            for m in range(mdl.f):
                #print('feature ' + mdl.metadata_dict[m] + " --> " + str(mdl.lambdas[k][m]) + " ")
                features[mdl.metadata_dict[m]]=mdl.lambdas[k][m]
                array_features.append(mdl.lambdas[k][m])
                if int(k) == 0:
                    #print('feature ' + mdl.metadata_dict[m])
                    col_features.append(mdl.metadata_dict[m])

            a = np.array(array_features)
            median=np.median(a)
            max=np.max(a)
            min=np.min(a)

            new_features=[]
            #new_features.append(k)
            for col in col_features:
                val = features[col]
                final_val = abs(max) + val + abs(median)
                features[col] = final_val
                #print("YYYYYY " + col + " :: " + str(features[col]))
                new_features.append(final_val)

            topics_features = topics_features.append(pd.Series(new_features), ignore_index=True)
            print("median " + str(median) + " : " + str(max) + " : " + str(min))

            for word, prob in mdl.get_topic_words(k):
                print('\t', word, prob, sep='\t')

        col_feaures = sorted(col_features, reverse=False)
        #col_features.insert(0,'Topic ID')
        topics_features.columns = col_features

        topics_features.to_csv('dmr_topic_year.csv', sep=',', encoding='utf-8')
        print(topics_features.head(20))

        df1_transposed = topics_features.T.rename_axis('Date').reset_index()
        #labels = []
        #for i in range(0,topic_number-1):
        #    labels.append('Topic_'+str(i))
        #df1_transposed.columns=labels

        import seaborn as sns
        import matplotlib.colors as mcolors

        print(df1_transposed.head(20))
        df1_transposed = df1_transposed.melt('Date', var_name='Topic', value_name='Importance Score')
        g = sns.relplot(x="Date", y="Importance Score", hue='Topic', dashes=False, markers=True,  data=df1_transposed, kind='line')

        output='dmr_topic.png'
        g.fig.suptitle('DMR Topic Model Results')
        g.savefig(output, format='png', dpi=500)
        # Show the plot
        plt.show()

        # calculate topic distribution for each metadata using softmax
        probs = np.exp(mdl.lambdas - mdl.lambdas.max(axis=0))
        probs /= probs.sum(axis=0)

        print('Topic distributions for each metadata')
        for f, metadata_name in enumerate(mdl.metadata_dict):
            print(metadata_name, probs[:, f], '\n')

        x = np.arange(mdl.k)
        width = 1 / (mdl.f + 2)

        fig, ax = plt.subplots()
        for f, metadata_name in enumerate(mdl.metadata_dict):
            ax.bar(x + width * (f - mdl.f / 2), probs[:, f], width, label=mdl.metadata_dict[f])

        ax.set_ylabel('Probabilities')
        ax.set_yscale('log')
        ax.set_title('Topic distributions')
        ax.set_xticks(x)
        ax.set_xticklabels(['Topic #{}'.format(k) for k in range(mdl.k)])
        ax.legend()

        fig.tight_layout()
        plt.show()

        return mdl

    def visualizeDMR(self, mdl, visual_result1='./result1.png', visual_result2='./result2.png'):
        # extract candidates for auto topic labeling
        extractor = tp.label.PMIExtractor(min_cf=10, min_df=5, max_len=5, max_cand=10000)
        cands = extractor.extract(mdl)

        # ranking the candidates of labels for a specific topic
        labeler = tp.label.FoRelevance(mdl, cands, min_df=5, smoothing=1e-2, mu=0.25)
        for k in range(mdl.k):
            print("== Topic #{} ==".format(k))
            print("Labels:", ', '.join(label for label, score in labeler.get_topic_labels(k, top_n=5)))
            for word, prob in mdl.get_topic_words(k, top_n=10):
                print(word, prob, sep='\t')
            print()

        # Init output
        topics_features = pd.DataFrame()
        col_features = []

        for k in range(mdl.k):
            print('Topic #{}'.format(k))
            array_features = []
            features = {}
            for m in range(mdl.f):
                # print('feature ' + mdl.metadata_dict[m] + " --> " + str(mdl.lambdas[k][m]) + " ")
                features[mdl.metadata_dict[m]] = mdl.lambdas[k][m]
                array_features.append(mdl.lambdas[k][m])
                if int(k) == 0:
                    # print('feature ' + mdl.metadata_dict[m])
                    col_features.append(mdl.metadata_dict[m])

            a = np.array(array_features)
            median = np.median(a)
            max = np.max(a)
            min = np.min(a)

            new_features = []
            # new_features.append(k)
            for col in col_features:
                val = features[col]
                final_val = abs(max) + val + abs(median)
                features[col] = final_val
                # print("YYYYYY " + col + " :: " + str(features[col]))
                new_features.append(final_val)

            topics_features = topics_features.append(pd.Series(new_features), ignore_index=True)
            print("median " + str(median) + " : " + str(max) + " : " + str(min))

            for word, prob in mdl.get_topic_words(k):
                print('\t', word, prob, sep='\t')

        col_feaures = sorted(col_features, reverse=False)
        # col_features.insert(0,'Topic ID')
        topics_features.columns = col_features

        topics_features.to_csv('dmr_topic_year.csv', sep=',', encoding='utf-8')
        print(topics_features.head(20))

        df1_transposed = topics_features.T.rename_axis('Date').reset_index()

        import seaborn as sns
        import matplotlib.colors as mcolors

        print(df1_transposed.head(20))
        df1_transposed = df1_transposed.melt('Date', var_name='Topic', value_name='Importance Score')
        g = sns.relplot(x="Date", y="Importance Score", hue='Topic', dashes=False, markers=True, data=df1_transposed,
                        kind='line')

        g.fig.suptitle('DMR Topic Model Results')
        g.savefig(visual_result1, format='png', dpi=500)
        # Show the plot
        plt.show()

        # calculate topic distribution for each metadata using softmax
        probs = np.exp(mdl.lambdas - mdl.lambdas.max(axis=0))
        probs /= probs.sum(axis=0)

        print('Topic distributions for each metadata')
        for f, metadata_name in enumerate(mdl.metadata_dict):
            print(metadata_name, probs[:, f], '\n')

        x = np.arange(mdl.k)
        width = 1 / (mdl.f + 2)

        fig, ax = plt.subplots()
        for f, metadata_name in enumerate(mdl.metadata_dict):
            ax.bar(x + width * (f - mdl.f / 2), probs[:, f], width, label=mdl.metadata_dict[f])

        ax.set_ylabel('Probabilities')
        ax.set_yscale('log')
        ax.set_title('Topic distributions')
        ax.set_xticks(x)
        ax.set_xticklabels(['Topic #{}'.format(k) for k in range(mdl.k)])
        ax.legend()

        fig.tight_layout()
        fig.savefig(visual_result2)

        plt.show()

    def inferLDATopicModel(self, model_file, unseen_words):

        mdl = tp.LDAModel.load(model_file)

        doc_inst = mdl.make_doc(unseen_words)
        topic_dist, ll = mdl.infer(doc_inst)
        print("Topic Distribution for Unseen Docs: ", topic_dist)
        print("Log-likelihood of inference: ", ll)

if __name__ == '__main__':

    import pyTextMiner as ptm

    mecab_path='C:\\mecab\\mecab-ko-dic'
    pipeline = ptm.Pipeline(ptm.splitter.NLTK(),
                            ptm.tokenizer.MeCab(mecab_path),
                            ptm.helper.POSFilter('NN*'),
                            ptm.helper.SelectWordOnly(),
                            ptm.helper.StopwordFilter(file='../stopwords/stopwordsKor.txt'))

    corpus = ptm.CorpusFromFieldDelimitedFileWithYear('../mallet/topic_input/sample_dmr_input.txt',doc_index=2,year_index=1)
    pair_map = corpus.pair_map

    result = pipeline.processCorpus(corpus.docs)
    text_data = []
    for doc in result:
        new_doc = []
        for sent in doc:
            for _str in sent:
                if len(_str) > 0:
                    new_doc.append(_str)
        text_data.append(new_doc)

    topic_number=20
    print('Running DMR')
    dmr_model_name='../test.lda.bin'
    topic_model = pyTextMinerTopicModel()

    #topic_model.dmr_model(text_data, pair_map, dmr_model_name, topic_number)
    topic_model.hdp_model(text_data, dmr_model_name)

    unseen_text='아사이 베리 블루베리 비슷하다'
    #topic_model.inferLDATopicModel(dmr_model_name, unseen_text)