import unittest
from textflint.input_layer.dataset import Dataset
from textflint.generation_layer.generator.pos_generator import POSGenerator

sample1 = {'x': ['That', 'is', 'a', 'pretty', 'prefixed', 'survey'],
           'y': ['DT', 'VBZ', 'DT', 'RB', 'JJ', 'NN']}
sample2 = {'x': ['That', 'is', 'a', 'prefixed', 'survey'],
           'y': ['DT', 'VBZ', 'DT', 'JJ', 'NN']}
sample3 = {'x': ['', '', ''],
           'y': ['O', 'O', 'O']}
sample4 = {'x': '! @ # $ % ^ & * ( )',
           'y': ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']}
special_data_sample = [sample3, sample4]
data_samples = [sample1, sample2]

dataset = Dataset('POS')
dataset.load(data_samples)
special_dataset = Dataset('POS')
special_dataset.load(special_data_sample)


class TestPOSGenerate(unittest.TestCase):

    def test_generate(self):
        # test MultiPOSSwap transformation
        gene = POSGenerator(transformation_methods=["SwapMultiPOS"],
                            subpopulation_methods=[],
                            transformation_config={"SwapMultiPOS":
                                        [{"treebank_tag": "NN"}]})
        for original_samples, trans_rst, trans_type in gene.generate(dataset):
            self.assertEqual(2, len(original_samples))
            self.assertEqual(2, len(trans_rst))
            for index in range(2):
                self.assertTrue(trans_rst[index].get_mask('x')[-1] == 2)
                self.assertTrue(trans_rst[index].get_words('x')[-1] !=
                                original_samples[index].get_words('x')[-1])

        # test PrefixSwap transformation
        gene = POSGenerator(transformation_methods=['SwapPrefix'],
                            subpopulation_methods=[])
        for original_samples, trans_rst, trans_type in gene.generate(dataset):
            self.assertEqual(2, len(original_samples))
            self.assertEqual(2, len(trans_rst))
            for index in range(2):
                self.assertTrue(trans_rst[index].get_mask('x')[-2] == 2)
                self.assertTrue(trans_rst[index].get_words('x')[-2] !=
                                original_samples[index].get_words('x')[-2])

        # test wrong transformation_methods
        gene = POSGenerator(transformation_methods=["wrong_transform_method"],
                            subpopulation_methods=[])
        self.assertRaises(ValueError, next, gene.generate(dataset))
        gene = POSGenerator(transformation_methods=["AddSubtree"],
                            subpopulation_methods=[])

        self.assertRaises(ValueError, next, gene.generate(dataset))
        gene = POSGenerator(transformation_methods="OOV",
                            subpopulation_methods=[])
        self.assertRaises(ValueError, next, gene.generate(dataset))

        # test empty dataset
        self.assertRaises(ValueError, next, gene.generate(Dataset('POS')))

        # test empty sample
        self.assertRaises(ValueError, next, gene.generate(special_dataset))


if __name__ == "__main__":
    unittest.main()
